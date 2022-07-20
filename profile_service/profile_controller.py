import json
import logging
from functools import wraps

import jwt
from flask import Blueprint, request, jsonify, current_app

from profile_svc import *

profile_controller = Blueprint('profile_controller', __name__)


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


@token_required
@profile_controller.route('/profile/save', methods=['POST'])
def save_profile():
    data = request.get_json()
    uid = data['uid']
    username = data['username']
    image = data['image']
    ctype = data['type']
    display_name = data['display_name']
    description = data['description']
    if len(ctype) > 0:
        save_avatar(username, image, ctype)
    add_profile(uid, username, display_name, description)

    return 'All details are saved'


@token_required
@profile_controller.route('/profile/getprof', methods=['POST'])
def get_profile():
    data = request.get_json()
    uid = data['uid']
    username = data['username']
    picture = get_avatar(username)
    profile = get_profile_by_id(uid)
    display_name = profile.display_name
    description = profile.description
    following = profile.following
    follower = profile.follower

    value = {
        "picture": picture,
        "display_name": display_name,
        "description": description,
        "following": following,
        "follower": follower
    }

    return json.dumps(value)


@token_required
@profile_controller.route('/profile/getuser', methods=["POST"])
def get_by_username():
    data = request.get_json()
    username = data['username']
    picture = get_avatar(username)
    profile = find_by_username(username)
    uid = profile.uid
    display_name = profile.display_name
    description = profile.description

    value = {
        "uid": uid,
        "picture": picture,
        "display_name": display_name,
        "description": description
    }

    return json.dumps(value)


@token_required
@profile_controller.route('/profile/follow', methods=['POST'])
def following():
    data = request.json
    uid: int = data["uid"]
    following_id: int = data["following_id"]
    add_following_response = add_new_following(uid, following_id)
    logging.info(add_following_response["message"])
    add_follower_response = add_new_follower(following_id, uid)
    logging.info(add_follower_response["message"])
    if add_follower_response["success"] and add_following_response["success"]:
        return {"success": True, "message": "User:{} has follow User:{}".format(uid, following_id)}
    else:
        return {"success": False, "message": "User:{} fail to follow User:{}".format(uid, following_id)}


@token_required
@profile_controller.route("/profile/unfollow", methods=["PATCH"])
def unfollow():
    data = request.json
    uid: int = data["uid"]
    remove_id: int = data["remove_id"]
    remove_following_response = remove_following(uid, remove_id)
    logging.info(remove_following_response["message"])
    remove_follower_response = remove_follower(remove_id, uid)
    logging.info(remove_follower_response["message"])
    return {"success": True}


@token_required
@profile_controller.route("/profile/getfollow", methods=["POST"])
def get_follow_info():
    data = request.json
    uid: int = data["uid"]
    follow = get_follow(uid)
    res = {"following": follow.following, "follower": follow.follower}
    return json.dumps(res)


@token_required
@profile_controller.route("/profile/getshort/<int:uid>", methods=["GET"])
def get_short(uid):
    profile = get_profile_by_id(uid)

    display_name = profile.display_name
    username = profile.username

    picture = get_avatar(username)

    value = {
        "username": username,
        "display_name": display_name,
        "picture": picture
    }

    return json.dumps(value)


@token_required
@profile_controller.route("/profile/savedPost", methods=['POST'])
def saved_post_controller():
    data = request.json
    uid: int = data["uid"]
    post_id: int = data["post_id"]
    return save_post(uid, post_id)


@token_required
@profile_controller.route("/profile/unsavedPost", methods=['PATCH'])
def unsaved_post_controller():
    data = request.json
    uid: int = data["uid"]
    post_id: int = data["post_id"]
    return unsaved_post(uid, post_id)


@token_required
@profile_controller.route("/profile/archive", methods=['POST'])
def get_archive():
    data = request.json
    uid: int = data["uid"]
    profile = get_profile_by_id(uid)
    return json.dumps(profile.post_id_archive)
