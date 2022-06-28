from flask import Blueprint
from flask import request

from model.user_account import UserAccount
from service import auth_svc

auth_controller = Blueprint('auth_controller', __name__)


@auth_controller.route('/register', methods=['POST'])
def register_route():
    data = request.json
    keys = ('username', 'password', 'firstname', 'lastname', 'phone_number')
    if data and all([k in data for k in keys]):
        account_obj = UserAccount(**data)
        status = auth_svc.register(account_obj)
        return {'status': status}
    return {'status': False}


@auth_controller.route('/auth', methods=['POST'])
def auth_route():
    credentials = request.json
    if credentials:
        status = auth_svc.authenticate(credentials.get('username'), credentials.get('password'))
        return {'status': status}
