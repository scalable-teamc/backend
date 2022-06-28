from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from controller.auth_controller import auth_controller

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/twitter_db"
database = SQLAlchemy()

login_manager = LoginManager()

if __name__ == '__main__':
    database.init_app(app)
    with app.app_context():
        database.create_all()
    login_manager.init_app(app)
    app.register_blueprint(auth_controller)

    # run app in debug mode on port 8082
    app.run(debug=True, port=8082)
