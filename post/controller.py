from flask import Flask, request
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy

import uuid
import json
from datetime import datetime
import psycopg2
import io
import os
import base64

from storage import MINIO_CLIENT

app = Flask(__name__)
CORS(app)
app.config[
    "SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/postgres"  # "postgresql://postgres:postgres@postgres:5432/postgres" #
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


###################
# Model
###################

class PasteModel(db.Model):
    postID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer())
    username = db.Column(db.String())
    likedUser = db.Column(db.ARRAY(db.Integer))
    content = db.Column(db.String())
    createdAt = db.Column(db.DateTime(), nullable=False, default=datetime.now)  # .now()

    # Return as dict to be send over HTTP response
    def to_dict(self):
        return {
            "postID": self.postID,
            "userID": self.userID,
            "username": self.username,
            "likedUser": self.likedUser,
            "content": self.content,
            "createdAt": self.createdAt
        }


@app.before_first_request
def create_tables():
    db.create_all()


###################
# Routes
###################

# Taking data from user, create post, and store it
# Parameters needed in incoming request: (userID, content, image, type, username, likedUser)
# What is kept in DB: (userID, content, postID, createAt, username, likedUser)
@app.route('/post', methods=['POST'])
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
@app.route('/get/<int:postID>', methods=['GET'])
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
@app.route('/get/<int:postID>/<int:userID>', methods=['GET'])
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
@app.route('/recent', methods=['POST'])
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


@app.route('/user-post/<int:uid>', methods=['GET'])
def get_user_post(uid):
    query = PasteModel.query.filter_by(userID=uid).order_by(PasteModel.createdAt.desc()).all()
    ret = []
    for row in query:
        ret.append(row.postID)
    return json.dumps(ret)


# Add userID to a post's likedUser array
# Parameters needed in incoming request: (postID, userID)
@app.route('/like', methods=['POST'])
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
@app.route('/unlike', methods=['POST'])
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


###################
# HELPER FUNCTIONS
###################

# Helper function for post_api()
def save_image(username_bucket, postID, image_file, ctype):
    if ctype == "":
        return

    img = base64.b64decode(bytes(image_file, 'utf-8'))
    ext = '.' + ctype.split('/')[1]
    size = len(img)
    img = io.BytesIO(img)

    # Save image to MINIO. Image name will be <postID>_image.ext
    MINIO_CLIENT.put_object(bucket_name=username_bucket, object_name=postID + "_image" + ext, data=img, length=size,
                            content_type=ctype)
    return ext
    # return username_bucket, postID, image_file, ctype


# Helper function for get_api() and recent_api()
def get_image(username_bucket, postID):
    content = ""
    content_type = ""
    # Get picture from MINIO
    for obj in MINIO_CLIENT.list_objects(bucket_name=username_bucket, prefix=str(postID) + "_image"):
        if obj is None:
            return None
        pic = MINIO_CLIENT.get_object(bucket_name=username_bucket, object_name=obj.object_name)
        content = base64.b64encode(pic.read()).decode('utf-8')
        ext = obj.object_name.split('.')[1]
        # content_type = "data:" + obj.content_type + ";base64,"
        content_type = "data:" + ext + ";base64,"
    return content_type + content
    # return str(username_bucket) + "_IMAGEIMAGE"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5466)

# Testing for 
# POST:
# curl -X POST http://127.0.0.1:5466/post -H 'Content-Type: application/json' -d '{ "userID": 777865, "username": "JackSparrow", "likedUser": [56, 6, 9906], "content": "Today is TESRTx", "image": null }'
# GET:
# curl -X GET http://127.0.0.1:5466/get/1
# LIKE:
# curl -X POST http://127.0.0.1:5466/like -H 'Content-Type: application/json' -d '{ "userID": 432, "postID": 1 }'
