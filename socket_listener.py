import os
import socket
import time

from dotenv import load_dotenv
from utils import Logger

load_dotenv()
URX_HOST = os.getenv("URX_HOST")
URX_PORT = int(os.getenv("URX_PORT"))

robot_ip = URX_HOST
robot_port = URX_PORT

logger = Logger("Socket Listener")

robot_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
robot_conn.connect((robot_ip, robot_port))

logger.info(f"Connected to robot at {robot_ip}:{robot_port}")

while True:
    data = robot_conn.recv(1024)
    if data is not None:
        if type(data) is bytes:
            try:
                logger.info(f"Message received: {data.decode('utf-8')}")
            except ValueError:
                logger.info(f"Message received: {data}")
        elif type(data) is str:
            logger.info(f"Message received: {data}")
    time.sleep(1)
