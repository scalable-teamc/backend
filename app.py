from flask import Flask

from controller.auth_controller import auth_controller

app = Flask(__name__)

app.register_blueprint(auth_controller)

if __name__ == '__main__':
    # run app in debug mode on port 8082
    app.run(debug=True, port=8082)
