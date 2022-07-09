from flask import Flask
from flask_socketio import SocketIO, emit
from feed import *
from feed_service import feed_db

async_mode = None
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/feed_db"
feed_db.init_app(app)
with app.app_context():
    feed_db.create_all()
    feed_db.session.commit()
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")
socketio.init_app(app, message_queue='redis://localhost:6379', cors_allowed_origins="*")


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


# @socketio.on('online')
# def set_online(uid):
#     add_online(uid)


# @socketio.on('offline')
# def set_offline(uid):
#     print('disconnected')
#     remove_online(uid)

# @socketio.event
# def disconnect():
#     emit('offline', 'f')


if __name__ == '__main__':
    socketio.run(app)
