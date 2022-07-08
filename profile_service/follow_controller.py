import logging

from flask import Blueprint, request

from .follow_svc import *

follower_controller = Blueprint('follow_controller', __name__)


@follower_controller.route('/follow/following', methods=['POST'])
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


@follower_controller.route("/follow/unfollow", methods=["PATCH"])
def unfollow():
    data = request.json
    uid: int = data["uid"]
    remove_id: int = data["remove_id"]
    remove_following_response = remove_following(uid, remove_id)
    logging.info(remove_following_response["message"])
    remove_follower_response = remove_follower(remove_id, uid)
    logging.info(remove_follower_response["message"])
    return {"success": True}
