from flask import Flask
from flask_login import LoginManager

from auth_service import user_db
from auth_service.auth_controller import auth_controller

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/user_db"
app.secret_key = "super secret key"

login_manager = LoginManager()

if __name__ == '__main__':
    user_db.init_app(app)
    with app.app_context():
        user_db.create_all()
        user_db.session.commit()
    login_manager.init_app(app)
    app.register_blueprint(auth_controller)

    # run app in debug mode on port 8082
    app.run(debug=True, port=8082)
