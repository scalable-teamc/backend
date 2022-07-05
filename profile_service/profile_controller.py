from flask import Blueprint, request
from .profile import *

profile_controller = Blueprint('profile_controller', __name__)


@profile_controller.route('/profile/save', methods=['POST'])
def save_profile():


    data = request.get_json()
    uid = data['uid']
    image = data['image']
    ctype = data['type']
    display_name = data['display_name']
    description = data['description']
    save_avatar(uid, image, ctype)
    add_display_name(uid,display_name)
    add_description(uid, description)
    return 'f'


@profile_controller.route('/profile/pic', methods=['GET'])
def get_pic():

    # frontend need to send uid somehow
    data = request.get_json()
    uid = data['uid']
    picture = get_avatar(uid)

    return picture

