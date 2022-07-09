from flask import Flask, session
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import redis

async_mode = None
app = Flask(__name__)
# CORS(app)
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")
socketio.init_app(app, message_queue='redis://localhost:6379', cors_allowed_origins="*")


# Receive the test request from client and send back a test response
@socketio.on('test_message')
def handle_message(data):
    print('received message: ' + str(data))
    send('test_response', {'data': 'Test response sent'})


# Broadcast a message to all clients
@socketio.on('broadcast_message')
def handle_broadcast(data):
    print('received')
    print(data)
    to = data['to']
    post_id = data['postID']
    emit(to, {'postID': post_id}, broadcast=True)


@socketio.event
def connect():
    emit('my_response', {'data': 'Connected'})


if __name__ == '__main__':
    socketio.run(app)
