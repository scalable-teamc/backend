from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from auth_init import user_db
from auth_controller import auth_controller
import os

url = "postgresql://" + os.environ["POSTGRES_USER"] + ":" + os.environ["POSTGRES_PASSWORD"] \
      + "@" + os.environ["POSTGRES_DB"] + "/user_db"

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    # app.run(debug=True, port=8082)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8082)
