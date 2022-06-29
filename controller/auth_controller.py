from flask import Blueprint, request

from service.auth_svc import *

auth_controller = Blueprint('auth_controller', __name__)


@auth_controller.route('/register', methods=['POST'])
def register_post():
    data = request.json
    username = data['username']
    password = data['password']
    return register(username, password)


@auth_controller.route('/login', methods=['POST'])
def login_post():
    credentials = request.json
    if credentials:
        username = credentials['username']
        password = credentials['password']
        return authenticate(username, password)
