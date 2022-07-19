from flask import Flask
from flask_cors import CORS

from profile_init import profile_db
from profile_controller import profile_controller
import os

url = "postgresql://" + os.environ["POSTGRES_USER"] + ":" + os.environ["POSTGRES_PASSWORD"] \
      + "@" + os.environ["POSTGRES_DB"] + "/profile_db"

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


if __name__ == '__main__':
    profile_db.init_app(app)
    with app.app_context():
        profile_db.create_all()
        profile_db.session.commit()
    app.register_blueprint(profile_controller)
    # run app in debug mode on port 8084
    # app.run(debug=True, port=8084)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8084)
