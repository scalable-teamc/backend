from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy

import uuid
import json
from datetime import datetime
import psycopg2

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] =  "postgresql://postgres:postgres@postgres:5432/postgres"
db = SQLAlchemy(app) 


class PasteModel(db.Model):
    postID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer(), autoincrement=True)
    mediaID = db.Column(db.Integer(), autoincrement=True)
    content = db.Column(db.String())
    createdAt = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow()) # .now()

    # Return as dict to be send over HTTP response
    def to_dict(self):
        return {
            "postID" : self.postID,
            "userID" : self.userID,
            "mediaID" : self.mediaID,
            "content" : self.content,
            "createdAt" : self.createdAt
        }

@app.before_first_request
def create_tables():
    db.create_all()

# Taking data from user, create post, and store it 
@app.route('/post', methods=['POST'])
def post_api():
    json_data = request.get_json()
    new_paste = PasteModel(userID=json_data["userID"], mediaID=json_data["mediaID"], content=json_data["content"])

    # Sent json_data to database
    db.session.add(new_paste)
    db.session.commit()

    return "Post created", 200 # return JSON data ID

# Get specific post (postID identifier for each Tweet)
@app.route('/get/<string:postID>', methods=['GET'])
def get_api(postID):
        result = PasteModel.query.filter_by(postID=postID).first()
        if not result:
            return "postID not found" , 404
        return result.to_dict(), 200

# Show most recent tweets
@app.route('/recent', methods=['POST'])
def recent_api():
    result = PasteModel.query.order_by("createdAt").limit(100)
    if not result:
        return "No post yet" , 404

    arr = []
    for i in result:
        arr.append(i.to_dict())
    return {"lst" : arr}, 200






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

# RESET DATABSE: Delete in Docker Volume

# TODO:
# - MinIO
# - Return only posts of followed users
# 
# 
# 

# Temp
# curl -X POST http://127.0.0.1:5000/post -H 'Content-Type: application/json' -d '{ "userID": 777865, "mediaID": 990999, "content": "Today is TESRTx" }'