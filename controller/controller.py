from email.policy import default
from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

from flask_sqlalchemy import SQLAlchemy

import uuid
import json
from datetime import datetime
import psycopg2

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] =  "postgresql://postgres:postgres@postgres:5432/postgres"
db = SQLAlchemy(app) 

# Used with @marshal_with(resource_fields), it turns returned PasteModel into JSON
resource_fields = {
	'postID': fields.String,
	'userID': fields.String,
	'content': fields.String,
	'createdAt': fields.DateTime
}


class PasteModel(db.Model):
    postID = db.Column(db.String(40), primary_key=True, default=str(uuid.uuid1()))
    userID = db.Column(db.String())
    content = db.Column(db.String())
    createdAt = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow()) # .now()

@app.before_first_request
def create_tables():
    db.create_all()


# Handles all incoming POST json for Post_API
post_api_args = reqparse.RequestParser()
post_api_args.add_argument("userID", type=str, help="ID of the user")
post_api_args.add_argument("content", type=str, help="Content of the twitter post")

class Post_API(Resource): # For POST , obtaining a data to create and store a twitter post

    def post(self):
        json_data = post_api_args.parse_args()

        new_id = str(uuid.uuid1())
        new_paste = PasteModel(postID=new_id , userID=json_data["userID"], content=json_data["content"])

        # Sent json_data to database
        db.session.add(new_paste)
        db.session.commit()

        return new_id, 200 # return JSON data ID


class Get_API(Resource): # For GET , 

    @marshal_with(resource_fields)
    def get(self): # get(self, paste_id):
        # result = PasteModel.query.filter_by(id=paste_id).first()
        # if not result:
        #     abort(404, message="No paste with such ID exists")

        result = {
            "Status":"GET Successful" 
        }

        return result, 200

    def post(self):
        result = PasteModel.query.order_by("createdAt").limit(100)
        arr = []
        for i in result:
            a_paste = {
                "postID" : i.postID,
                "userID" : i.userID,
                "content" : i.content,
                "createdAt" : str(i.createdAt)
            }
            arr.append(a_paste)
        return arr, 200
        # return {"id":new_id}, 200 # return JSON data ID




# Add this Resource to the API
api.add_resource(Post_API, "/post")
api.add_resource(Get_API, "/get") 


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


# TODO:
# - Postgres DB
# - MinIO
# - User handling
# - CLean up requirements.py
# 
# 
# 
