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
    print(data)
    to = data['to']
    post_id = data['postID']
    add_feed(to, post_id, data['date'])
    sent = []
    for online in get_online_by_uid(to):
        if (to == online.uid) and (to not in sent):
            sent.append(to)
            print(to)
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
    return json.dumps(ret)


@socketio.on('online')
def set_online(uid):
    print(request.sid)
    add_online(uid, request.sid)


@socketio.on('logout')
def set_offline():
    print('Logged out')
    remove_online(request.sid)


@socketio.event
def disconnect():
    remove_online(request.sid)
    print(request.sid)
    print("Disconnected")


if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()
    import eventlet.wsgi
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    # socketio.run(app)
