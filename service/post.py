from flask_sqlalchemy import SQLAlchemy

import uuid
import json
from datetime import datetime
import psycopg2

from model import database as db
from model.post_model import PasteModel


# Taking data from user, create post, and store it. Return str
def create_post(json_data):
    new_id = str(uuid.uuid1())
    new_paste = PasteModel(postID=new_id , userID=json_data["userID"], mediaID=json_data["mediaID"], content=json_data["content"])

    # Sent json_data to database
    db.session.add(new_paste)
    db.session.commit()

    return new_id # return JSON data ID


# Get specific post (postID identifier for each Tweet). Return dict
def get_specific_post(postID: str):
        result = PasteModel.query.filter_by(postID=postID).first()
        if not result:
            return None
        return result.to_dict()


# Show most recent tweets. Return array of dict
def get_recent_posts(): 
    result = PasteModel.query.order_by("createdAt").limit(100)
    if not result:
        return None

    arr = []
    for i in result:
        arr.append(i.to_dict())
    return arr







