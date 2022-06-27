from flask import request

from app import app
from model.user_account import UserAccount
from service import auth_svc


@app.route('/register', methods=['POST'])
def register_controller():
    data = request.json
    keys = ('username', 'password', 'firstname', 'lastname', 'phone_number')
    if data and all([k in data for k in keys]):
        account_obj = UserAccount(**data)
        status = auth_svc.register(account_obj)
        return {'status': status}
    return {'status': False}


@app.route('/auth', methods=['POST'])
def auth_controller():
    credentials = request.json
    if credentials:
        status = auth_svc.authenticate(credentials.get('username'), credentials.get('password'))
        return {'status': status}
