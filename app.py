from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/twitter_db"
database = SQLAlchemy()

if __name__ == '__main__':
    database.init_app(app)
    database.create_all()
    # run app in debug mode on port 8082
    app.run(debug=True, port=8082)
