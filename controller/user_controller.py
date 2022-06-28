from flask import Blueprint
from flask import request

from service.auth_svc import *

user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/register', methods=['POST'])
def register_route():
    data = request.json
    username = data['username']
    password = data['password']
    return register(username, password)


@user_controller.route('/auth', methods=['POST'])
def auth_route():
    credentials = request.json
    if credentials:
        username = credentials['username']
        password = credentials['password']
        status = authenticate(username, password)
        return {'status': status}
    return {'status': False}
