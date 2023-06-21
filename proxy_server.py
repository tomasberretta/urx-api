import socketio
from dotenv import load_dotenv
from scapy.all import *
from utils import Logger

load_dotenv()
URX_HOST = os.getenv("URX_HOST")
URX_PORT = int(os.getenv("URX_PORT"))
FLASK_HOST = os.getenv("FLASK_HOST")
FLASK_PORT = int(os.getenv("FLASK_PORT"))
PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = int(os.getenv("PROXY_PORT"))
WEBSOCKET_HOST = os.getenv("WEBSOCKET_HOST")
WEBSOCKET_PORT = os.getenv("WEBSOCKET_PORT")

logger = Logger("Proxy Server")

# Define the IP and port of the http server and the robot
http_ip = FLASK_HOST
http_port = FLASK_PORT
robot_ip = URX_HOST
robot_port = URX_PORT

logger.info(f"Starting proxy server at {PROXY_HOST}:{PROXY_PORT}")

# Create a socket object for the proxy server
proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy.bind((PROXY_HOST, PROXY_PORT))  # Bind the proxy to any interface and port 8080
proxy.listen(5)  # Listen for incoming connections

# Accept a connection from the http server
http_conn, http_addr = proxy.accept()
logger.info(f"Connected to http server at {http_addr}")

# Connect to the robot
robot_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
robot_conn.connect((robot_ip, robot_port))
logger.info(f"Connected to robot at {robot_ip}:{robot_port}")

# Create a socket io client object
sio = socketio.Client()

# Define a function to handle socket io connections
@sio.event
def connect():
    pass


# Define a function to handle socket io messages
@sio.event
def message(data):
    pass


# Connect to the socket io server
sio.connect(f"http://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")

logger.info(f"Proxy server successfully started at {PROXY_HOST}:{PROXY_PORT}")


# Create a function to forward data from one socket to another
def forward_data(src, dst):
    data = src.recv(1024)  # Receive up to 1024 bytes of data from the source socket
    if data:  # If there is any data
        logger.info(f"Forwarding {len(data)} bytes of data from {src.getpeername()} to {dst.getpeername()}")
        logger.info(data)
        # Send a message to the socket io server
        sio.send(data)
        dst.send(data)  # Send the data to the destination socket
        return True  # Return True to indicate success
    else:  # If there is no data
        logger.info(f"Closing connection from {src.getpeername()}")
        src.close()  # Close the source socket
        dst.close()  # Close the destination socket
        return False  # Return False to indicate failure


# Create a loop to forward data between the http server and the robot
while True:
    # Use select to wait for data on either socket
    ready_sockets, _, _ = select.select([http_conn, robot_conn], [], [])
    for sock in ready_sockets:  # For each socket that has data
        if sock == http_conn:  # If it is the http server socket
            # Forward data from the http server to the robot
            if not forward_data(http_conn, robot_conn):
                break  # Break the loop if the connection is closed
        elif sock == robot_conn:  # If it is the robot socket
            # Forward data from the robot to the http server
            if not forward_data(robot_conn, http_conn):
                break  # Break the loop if the connection is closed

# Close the proxy socket
proxy.close()
logger.info("Proxy server stopped")
