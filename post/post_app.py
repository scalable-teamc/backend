from flask import Flask
from flask_cors import CORS

from post_init import post_db
from post_controller import post_controller
import os

url = "postgresql://" + os.environ["POSTGRES_USER"] + ":" + os.environ["POSTGRES_PASSWORD"] \
      + "@" + os.environ["POSTGRES_DB"] + "/post_db"

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


if __name__ == "__main__":
    post_db.init_app(app)
    with app.app_context():
        post_db.create_all()
        post_db.session.commit()
    app.register_blueprint(post_controller)
    # app.run(host='0.0.0.0', port=5466)
    from waitress import serve
    serve(app, host="0.0.0.0", port=5466)
