from functools import wraps
import jwt
import json
from flask import Blueprint, request, jsonify, current_app
from post_db import *
from post_helper import *
post_controller = Blueprint('post_controller', __name__)


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization')

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        try:
            token = auth_headers
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401
    return _verify


# Taking data from user, create post, and store it
# Parameters needed in incoming request: (userID, content, image, type, username, likedUser)
# What is kept in DB: (userID, content, postID, createAt, username, likedUser)
@token_required
@post_controller.route('/post', methods=['POST'])
def post_api():
    json_data = request.get_json()

    new_paste = PasteModel(userID=json_data["userID"], username=json_data["username"], likedUser="",
                           content=json_data["content"])

    # Sent json_data to database
    db.session.add(new_paste)
    db.session.commit()

    # Saving media (If there's no image, json_data['image'] == None)
    image = json_data['image']
    if image is not None:
        username = json_data["username"]
        id_of_post = str(new_paste.to_dict()["postID"])
        image = json_data["image"]
        ctype = json_data['type']

        save_image(username_bucket=username, postID=id_of_post, image_file=image, ctype=ctype)

    return str(new_paste.postID), 200  # return JSON data ID


# Get specific post (postID identifier for each Tweet)
# Response dict will contain: (userID, content, image, postID, createAt)
# image is not kept in DB, but fetched from MINIO upon every get request
@token_required
@post_controller.route('/get/<int:postID>', methods=['GET'])
def get_api(postID):
    result = PasteModel.query.filter_by(postID=postID).first()
    if not result:
        return "postID not found\n", 404
    final = result.to_dict()

    # Fetch media and add in new parameters
    username = final["username"]
    final["image"] = get_image(username, final["postID"])

    return final, 200


# Get specific post AND whether the user liked the requested post
# Response dict will contain: (userID, content, image, postID, createAt)
# image is not kept in DB, but fetched from MINIO upon every get request
@token_required
@post_controller.route('/get/<int:postID>/<int:userID>', methods=['GET'])
def get_api_user_liked(postID, userID):
    result = PasteModel.query.filter_by(postID=postID).first()
    if not result:
        return "postID not found\n", 404
    final = result.to_dict()

    # Fetch media and add in new parameters
    username = final["username"]
    final["image"] = get_image(username, final["postID"])

    didUserLike = False
    if userID in final["likedUser"]:
        didUserLike = True

    final["isLiked"] = didUserLike

    return final, 200


# Show most recent tweets
@token_required
@post_controller.route('/recent', methods=['POST'])
def recent_api():
    result = PasteModel.query.order_by("createdAt").limit(100)
    if not result:
        return "No post yet\n", 404

    arr = []
    for i in result:
        aPost = i.to_dict()

        # Add pictures if there's any
        username = aPost["username"]
        aPost["image"] = get_image(username)

        arr.append(aPost)
    return {"lst": arr}, 200


# Add userID to a post's likedUser array
# Parameters needed in incoming request: (postID, userID)
@token_required
@post_controller.route('/like', methods=['POST'])
def like_post():
    # Get post
    json_data = request.get_json()
    post = PasteModel.query.filter_by(postID=json_data["postID"]).first()
    if not post:
        return "postID not found\n", 404

    # Updates post
    post.likedUser = post.likedUser + [json_data["userID"]]
    db.session.commit()

    return "New Like!\n", 200


# Remove userID from a post's likedUser array
# Parameters needed in incoming request: (postID, userID)
@token_required
@post_controller.route('/unlike', methods=['POST'])
def unlike_post():
    # Get post
    json_data = request.get_json()
    post = PasteModel.query.filter_by(postID=json_data["postID"]).first()
    if not post:
        return "postID not found\n", 404

    # Updates post
    target = json_data["userID"]
    if target in post.likedUser:
        newArr = post.likedUser[:]
        newArr.remove(target)
        post.likedUser = newArr
    else:
        return "userID hasn't liked this post\n", 404

    db.session.commit()

    return "Unliked!\n", 200


@token_required
@post_controller.route('/user-post/<int:uid>', methods=['GET'])
def get_user_post(uid):
    query = PasteModel.query.filter_by(userID=uid).order_by(PasteModel.createdAt.desc()).all()
    ret = []
    for row in query:
        ret.append(row.postID)
    return json.dumps(ret)
