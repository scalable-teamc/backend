from email.policy import default
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
    postID = db.Column(db.String(40), primary_key=True, default=str(uuid.uuid1()))
    userID = db.Column(db.String())
    content = db.Column(db.String())
    createdAt = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow()) # .now()

@app.before_first_request
def create_tables():
    db.create_all()

# For POST: receiving JSON
@app.route('/post', methods=['POST'])
def post_api():
    json_data = request.get_json()
    new_id = str(uuid.uuid1())
    new_paste = PasteModel(postID=new_id , userID=json_data["userID"], content=json_data["content"])

    # Sent json_data to database
    db.session.add(new_paste)
    db.session.commit()

    return new_id, 200 # return JSON data ID

# Show all recent ones
@app.route('/recent', methods=['POST'])
def recent_api():
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
    return {"lst" : arr}, 200



# class Get_API(Resource): # For GET , 

#     @marshal_with(resource_fields)
#     def get(self): # get(self, paste_id):
#         # result = PasteModel.query.filter_by(id=paste_id).first()
#         # if not result:
#         #     abort(404, message="No paste with such ID exists")

#         result = {
#             "Status":"GET Successful" 
#         }

#         return result, 200





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


# TODO:
# - Postgres DB
# - MinIO
# - CLean up requirements.py
# 
# 
# 

