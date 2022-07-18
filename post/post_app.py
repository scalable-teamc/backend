from flask import Flask
from flask_cors import CORS

from post import post_db
from post.post_controller import post_controller

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/postgres"  # "postgresql://postgres:postgres@postgres:5432/postgres" #
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
