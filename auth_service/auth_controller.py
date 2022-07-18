from flask import Blueprint, request

from auth_svc import *

auth_controller = Blueprint('auth_controller', __name__)


@auth_controller.route('/auth/register', methods=['POST'])
def register_post():
    data = request.json
    username = data['username']
    password = data['password']
    return register(username, password)


@auth_controller.route('/auth/login', methods=['POST'])
def login_post():
    credentials = request.json
    if credentials:
        username = credentials['username']
        password = credentials['password']
        return authenticate(username, password)


@auth_controller.route('/auth/remove', methods=['DELETE'])
def user_delete():
    data = request.json
    username = data['username']
    return remove_user(username)
