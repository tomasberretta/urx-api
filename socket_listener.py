import os
import socket
import time

from dotenv import load_dotenv

from logger import Logger

load_dotenv()
URX_HOST = os.getenv("URX_HOST")
URX_PORT = int(os.getenv("URX_PORT"))
LISTENER_SLEEP_TIME = int(os.getenv("LISTENER_SLEEP_TIME")) if os.getenv("LISTENER_SLEEP_TIME") and int(
    os.getenv("LISTENER_SLEEP_TIME")) >= 0 else 1

logger = Logger("Socket Listener")

robot_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    robot_conn.connect((URX_HOST, URX_PORT))
except ConnectionRefusedError:
    logger.error(f"Failed to connect to robot at {URX_HOST}:{URX_PORT}")
    exit(1)

logger.info(f"Connected to robot at {URX_HOST}:{URX_PORT}")

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
    time.sleep(LISTENER_SLEEP_TIME)
