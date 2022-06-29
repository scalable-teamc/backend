from flask import Flask, request, Blueprint

from flask_sqlalchemy import SQLAlchemy

import uuid
import json
from datetime import datetime
import psycopg2

post_controller = Blueprint('post_controller', __name__)

post_controller.config["SQLALCHEMY_DATABASE_URI"] =  "postgresql://postgres:postgres@postgres:5432/postgres"
db = SQLAlchemy(post_controller)


class PasteModel(db.Model):
    postID = db.Column(db.String(40), primary_key=True, default=str(uuid.uuid1()))
    userID = db.Column(db.String(40))
    mediaID = db.Column(db.String(40))
    content = db.Column(db.String())
    createdAt = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow()) # .now()

    # Return as dict to be send over HTTP response
    def to_dict(self):
        return {
            "postID" : self.postID,
            "userID" : self.userID,
            "mediaID" : self.mediaID,
            "content" : self.content,
            "createdAt" : str(self.createdAt)
        }

# Taking data from user, create post, and store it 
@post_controller.route('/post', methods=['POST'])
def post_api():
    json_data = request.get_json()
    new_id = str(uuid.uuid1())
    new_paste = PasteModel(postID=new_id , userID=json_data["userID"], mediaID=json_data["mediaID"], content=json_data["content"])

    # Sent json_data to database
    db.session.add(new_paste)
    db.session.commit()

    return new_id, 200 # return JSON data ID

# Get specific post (postID identifier for each Tweet)
@post_controller.route('/get/<string:postID>', methods=['GET'])
def get_api(postID):
        result = PasteModel.query.filter_by(postID=postID).first()
        if not result:
            return "postID not found" , 404
        return result.to_dict(), 200

# Show most recent tweets
@post_controller.route('/recent', methods=['POST'])
def recent_api():
    result = PasteModel.query.order_by("createdAt").limit(100)
    if not result:
        return "No post yet" , 404

    arr = []
    for i in result:
        arr.append(i.to_dict())
    return {"lst" : arr}, 200




# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)


# TODO:
# - MinIO
# - Return only posts of followed users

# TODO:
# - See if putting DB config in here works
# - Move PasteModel to /model
# - Dockerfile and etc.
# - General refactor


# Temp
# curl -X POST http://127.0.0.1:5000/post -H 'Content-Type: application/json' -d '{ "userID": "abcdefghijkpqrstxyz", "mediaID": "kokoaksoskao", "content": "Today is Sunday" }'