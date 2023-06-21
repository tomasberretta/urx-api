import os
from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO, emit
from utils import Logger

load_dotenv()
WEBSOCKET_HOST = os.getenv("WEBSOCKET_HOST")
WEBSOCKET_PORT = os.getenv("WEBSOCKET_PORT")

# Create a Flask app object
app = Flask(__name__)

# Create a SocketIO app object
socketio = SocketIO(app)

logger = Logger("Socket Server")

# Define a route for the index page
@app.route('/')
def index():
    return "Hello, this is the socket io server"


# Define a function to handle socket io connections
@socketio.on('connect')
def handle_connect():
    logger.info("Connected to the socket io server")
    emit('welcome', {'message': 'Welcome to the socket io server'})


# Define a function to handle socket io messages
@socketio.on('message')
def handle_message(data):
    if data is not None:
        if type(data) is bytes:
            try:
                logger.info(f"Message received: {data.decode('utf-8')}")
                socketio.send('Message received: ' + data.decode('utf-8'))
            except ValueError:
                logger.info(f"Message received: {data}")
                socketio.send('Message received: ' + data)
        elif type(data) is str:
            logger.info(f"Message received: {data}")
            socketio.send('Message received: ' + data)


# Run the socket io server
if __name__ == '__main__':
    logger.info(f"Flask socket io server starting at {WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    socketio.run(app, host=WEBSOCKET_HOST, port=WEBSOCKET_PORT)
