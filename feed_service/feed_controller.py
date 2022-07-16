import json

from flask import Flask, request
from flask_socketio import SocketIO, emit
from feed import *
from feed_service import feed_db
from flask_cors import CORS

# async_mode = None
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/feed_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
feed_db.init_app(app)
with app.app_context():
    feed_db.create_all()
    feed_db.session.commit()
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")
socketio.init_app(app, message_queue='redis://127.0.0.1:6379', cors_allowed_origins="*")


# Broadcast a message to all clients
@socketio.on('broadcast_message')
def handle_broadcast(data):
    print('received')
    print(data)
    to = data['to']
    post_id = data['postID']
    add_feed(to, post_id, data['date'])
    emit(to, {'postID': post_id}, broadcast=True)


@socketio.event
def connect():
    emit('my_response', {'data': 'Connected'})


@app.route('/feed/all', methods=['POST'])
def get_all_feed():
    data = request.get_json()
    uid = data['uid']
    offset = data['offset']
    ret = []
    for feed in get_feed_by_uid(uid, offset):
        ret.append(feed.post_id)
    print(ret)
    return json.dumps(ret)

# @socketio.on('online')
# def set_online(uid):
#     add_online(uid)


# @socketio.on('offline')
# def set_offline(uid):
#     print('disconnected')
#     remove_online(uid)

# @socketio.event
# def disconnect():
#     print("Disconnected")


if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()
    import eventlet.wsgi
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    # socketio.run(app)
