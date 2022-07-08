from flask import Flask, request
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy

import uuid
import json
from datetime import datetime
import psycopg2
import io
import os
import base64

from storage import MINIO_CLIENT

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] =  "postgresql://postgres:password@localhost:5432/postgres" # "postgresql://postgres:postgres@postgres:5432/postgres" #
db = SQLAlchemy(app)


class PasteModel(db.Model):
    postID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer())
    username = db.Column(db.String())
    content = db.Column(db.String())
    createdAt = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())  # .now()

    # Return as dict to be send over HTTP response
    def to_dict(self):
        return {
            "postID": self.postID,
            "userID": self.userID,
            "username": self.username,
            "content": self.content,
            "createdAt": self.createdAt
        }


@app.before_first_request
def create_tables():
    db.create_all()


# Taking data from user, create post, and store it
# Parameters needed in incoming request: (userID, content, image, type, username)
# What is kept in DB: (userID, content, postID, createAt)
@app.route('/post', methods=['POST'])
def post_api():
    json_data = request.get_json()

    new_paste = PasteModel(userID=json_data["userID"], username=json_data["username"], content=json_data["content"])

    # Sent json_data to database
    db.session.add(new_paste)
    db.session.commit()

    # Saving media (If there's no image, json_data['image'] == None)
    image = json_data['image']
    if image is not None:

        username = json_data["username"]
        id_of_post = str(new_paste.to_dict()["postID"])
        image = json_data["image"]
        ctype = json_data['type']

        save_image(username_bucket=username, postID=id_of_post, image_file=image, ctype=ctype)

    return "Post created\n", 200  # return JSON data ID

# Helper function for post_api()
def save_image(username_bucket, postID, image_file, ctype):
    if ctype == "":
        return

    img = base64.b64decode(bytes(image_file, 'utf-8'))
    ext = '.' + ctype.split('/')[1]
    size = len(img)
    img = io.BytesIO(img)

    # Save image to MINIO. Image name will be <postID>_image.ext
    MINIO_CLIENT.put_object(bucket_name=username_bucket, object_name=postID + "_image" + ext, data=img, length=size, content_type=ctype)
    return ext
    # return username_bucket, postID, image_file, ctype



# Get specific post (postID identifier for each Tweet)
# Response dict will contain: (userID, content, image, postID, createAt)
# image is not kept in DB, but fetched from MINIO upon every get request
@app.route('/get/<int:postID>', methods=['GET'])
def get_api(postID):
    result = PasteModel.query.filter_by(postID=postID).first()
    if not result:
        return "postID not found\n", 404
    final = result.to_dict()

    # Fetch media and add in new parameters
    username = final["username"]
    final["image"] = get_image(username, final["postID"])

    return final, 200

# Helper function for get_api() and recent_api()
def get_image(username_bucket, postID):
    content = ""
    content_type = ""
    # Get picture from MINIO
    for obj in MINIO_CLIENT.list_objects(bucket_name=username_bucket, prefix=postID+"_image"):
        if obj is None:
            return None
        pic = MINIO_CLIENT.get_object(bucket_name=username_bucket, object_name=obj.object_name)
        content = base64.b64encode(pic.read()).decode('utf-8')
        ext = obj.object_name.split('.')[1]
        # content_type = "data:" + obj.content_type + ";base64,"
        content_type = "data:" + ext + ";base64,"
    return content_type + content
    # return str(username_bucket) + "_IMAGEIMAGE"


# Show most recent tweets
@app.route('/recent', methods=['POST'])
def recent_api():
    result = PasteModel.query.order_by("createdAt").limit(100)
    if not result:
        return "No post yet\n", 404

    arr = []
    for i in result:
        aPost = i.to_dict()

        # Add pictures if there's any
        username = aPost["username"]
        aPost["image"] = get_image(username)

        arr.append(aPost)
    return {"lst": arr}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5466)

# Testing for 
# POST:
# curl -X POST http://127.0.0.1:5466/post -H 'Content-Type: application/json' -d '{ "userID": 777865, "username": "JackSparrow", "content": "Today is TESRTx" }'
# curl -X POST http://127.0.0.1:5466/post -H 'Content-Type: application/json' -d '{ "userID": 777865, "username": "JackSparrow", "content": "Today is TESRTx", "image": null }'
# GET:
# curl -X GET http://127.0.0.1:5466/get/1
