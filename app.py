from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from controller.user_controller import user_controller

app = Flask(__name__)
app.register_blueprint(user_controller)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/twitter_db"
database = SQLAlchemy()

if __name__ == '__main__':
    database.init_app(app)
    database.create_all()
    # run app in debug mode on port 8082
    app.run(debug=True, port=8082)
