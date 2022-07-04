from storage import MINIO_CLIENT
from flask import Blueprint, request
from .profile import *

profile_controller = Blueprint('profile_controller', __name__)

@profile_controller.route('/profile/save', methods=['POST'])
def get_avatar():

    data = request.get_json()
    save_avatar(data, 'test')
    return get_avatar_file('test')