from flask import Flask, request, Blueprint

from flask_sqlalchemy import SQLAlchemy

import uuid
import json
from datetime import datetime
import psycopg2

from post.post import *

post_controller = Blueprint('post_controller', __name__)
# post_controller.config["SQLALCHEMY_DATABASE_URI"] =  "postgresql://postgres:postgres@postgres:5432/postgres"
# db = SQLAlchemy(post_controller)



# Response: ID of newly created post as str
@post_controller.route('/post', methods=['POST'])
def post_api():
    json_data = request.get_json()
    result = create_post(json_data) # result will be postID
    return result, 200 

# Response: requested post in the format of dict
@post_controller.route('/get/<string:postID>', methods=['GET'])
def get_api(postID):
    result = get_specific_post(postID) # result will be dict
    if result is None:
        return "postID not found" , 404
    return result, 200

# Response: dict whose value is array of posts
@post_controller.route('/recent', methods=['POST'])
def recent_api():
    result = get_recent_posts()
    if result is None:
        return "No post yet" , 404
    return {"lst" : result}, 200




# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)


# TODO:
# - MinIO
# - Return only posts of followed users

# TODO:
# - See if putting DB config in here works
# - Dockerfile and etc.


# Temp
# # curl -X POST http://127.0.0.1:5000/post -H 'Content-Type: application/json' -d '{ "userID": 777865, "mediaID": 990999, "content": "Today is TESRTx" }' 