from storage import MINIO_CLIENT
from flask import Blueprint, request
from .profile import *

profile_controller = Blueprint('profile_controller', __name__)


@profile_controller.route('/profile/save', methods=['POST'])
def get_avatar():

    data = request.get_json()
    uid = data['uid']
    image = data['image']
    save_avatar(uid, image)
    return get_avatar_file(uid)