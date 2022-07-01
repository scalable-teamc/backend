from flask import Flask
from flask_login import LoginManager

from controller.post_controller import post_controller

app = Flask(__name__)

login_manager = LoginManager()

if __name__ == '__main__':
    app.register_blueprint(post_controller)

    # run app in debug mode on port 8080
    app.run(debug=True, port=8080)
