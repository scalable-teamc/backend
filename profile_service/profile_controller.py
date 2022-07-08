import json
import logging

from flask import Blueprint, request

from .profile import *

profile_controller = Blueprint('profile_controller', __name__)


@profile_controller.route('/profile/save', methods=['POST'])
def save_profile():
    data = request.get_json()
    uid = data['uid']
    username = data['username']
    image = data['image']
    ctype = data['type']
    display_name = data['display_name']
    description = data['description']
    save_avatar(username, image, ctype)
    add_profile(uid, username, display_name, description)

    return 'All details are saved'


@profile_controller.route('/profile/getprof', methods=['POST'])
def get_profile():
    data = request.get_json()
    uid = data['uid']
    username = data['username']
    picture = get_avatar(username)
    profile = get_profile_by_id(uid)
    display_name = profile.display_name
    description = profile.description

    value = {
        "picture": picture,
        "display_name": display_name,
        "description": description
    }

    return json.dumps(value)


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


@profile_controller.route('/profile/following', methods=['POST'])
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
    remove_following(uid, following_id)
    remove_follower(following_id, uid)
    return {"success": False, "message": "User:{} fail to follow User:{}".format(uid, following_id)}


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
