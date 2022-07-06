import json

from flask import Blueprint, request
from .profile import *

profile_controller = Blueprint('profile_controller', __name__)


@profile_controller.route('/profile/save', methods=['POST'])
def save_profile():

    data = request.get_json()
    uid = data['uid']
    username = data['username']
    image = data['image']
    type = data['type']
    display_name = data['display_name']
    description = data['description']
    save_avatar(username, image, type)
    add_profile(uid, display_name, description)

    return 'All details are saved'


@profile_controller.route('/profile/getprof', methods=['POST'])
def get_profile():

    data = request.get_json()
    uid = data['uid']
    username = data['username']
    picture = get_avatar(username)
    display_name = get_display_name(uid)
    description = get_description(uid)

    value = {
        "picture": picture,
        "display_name": display_name,
        "description": description
    }

    return json.dumps(value)


# @profile_controller.route('/profile/pic', methods=['GET'])
# def get_pic():
#
#     # frontend need to send uid somehow
#     data = request.get_json()
#     uid = data['uid']
#     picture = get_avatar(uid)
#
#     return picture
#
#
# @profile_controller.route('/profile/disname', methods=['GET'])
# def get_disp():
#
#     # frontend need to send uid somehow
#     data = request.get_json()
#     uid = data['uid']
#     display_name = get_display_name(uid)
#
#     return display_name
#
#
# @profile_controller.route('/profile/description', methods=['GET'])
# def get_desc():
#
#     # frontend need to send uid somehow
#     data = request.get_json()
#     uid = data['uid']
#     description = get_description(uid)
#
#     return description