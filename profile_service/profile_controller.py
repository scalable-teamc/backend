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
