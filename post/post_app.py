from flask import Flask

from post.post_controller import post_controller

app = Flask(__name__)


if __name__ == '__main__':
    app.register_blueprint(post_controller)

    # run app in debug mode on port 8086
    app.run(debug=True, port=8086)
