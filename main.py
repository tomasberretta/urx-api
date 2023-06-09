import json
import os
from logging.config import dictConfig
from flask import Flask, request
from dotenv import load_dotenv

from urx_service import UrxEService
from utils import ApiResponse

load_dotenv()

# This configuration should only be used in development
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
urx_service = UrxEService()


class Logger:
    def info(self, message):
        print(message)

    def error(self, message):
        print(message)

    def warning(self, message):
        print(message)

    def debug(self, message):
        print(message)


class FlaskLogger(Logger):
    def __init__(self, app):
        self._app = app

    def info(self, message):
        self._app.logger.info(message)

    def error(self, message):
        self._app.logger.error(message)

    def warning(self, message):
        self._app.logger.warning(message)

    def debug(self, message):
        self._app.logger.debug(message)


@app.route('/health', methods=['GET'])
def health():
    return json.loads('{"status": "ok"}'), 200


@app.route('/health-connection', methods=['GET'])
def health_check():
    return urx_service.health_check()
    # return json.loads('{"status": "ok"}'), 200


@app.route('/ur5e/gripper/partial', methods=['POST'])
def partial():
    app.logger.info('Entered POST /ur5e/gripper/partial')
    amount = request.get_json()['amount']
    app.logger.info('Received partial with amount: %s', amount)
    if amount > 255 or amount < 0:
        raise Exception("Amount must be between 0 and 255")
    else:
        urx_service.partial_gripper(amount=amount)
    return ApiResponse(200, {"status": f"gripper partially moved to {amount}"}).to_json()


@app.route('/ur5e/gripper/open', methods=['POST'])
def open():
    app.logger.info('Entered POST /ur5e/gripper/open')
    urx_service.open_gripper()
    return ApiResponse(200, {"status": "fully open"}).to_json()


@app.route('/ur5e/gripper/close', methods=['POST'])
def close():
    app.logger.info('Entered POST /ur5e/gripper/close')
    urx_service.close_gripper()
    return ApiResponse(200, {"status": "fully closed"}).to_json()


@app.route('/ur5e/movej', methods=['POST'])
def movej():
    app.logger.info('Entered POST /ur5e/movej')
    coordinates = request.get_json()['coordinates']
    angles = request.get_json()['angles']
    acceleration = request.get_json()['acceleration']
    velocity = request.get_json()['velocity']
    app.logger.info('Received movej: %s', f"[{coordinates} {angles}], {acceleration}, {velocity}")
    urx_service.movej(coordinates, angles, acceleration, velocity)
    return ApiResponse(200, {"status": f"moved"}).to_json()


@app.route('/ur5e/movel', methods=['POST'])
def movel():
    app.logger.info('Entered POST /ur5e/movel')
    coordinates = request.get_json()['coordinates']
    angles = request.get_json()['angles']
    acceleration = request.get_json()['acceleration']
    velocity = request.get_json()['velocity']
    app.logger.info('Received movel: %s', f"[{coordinates} {angles}], {acceleration}, {velocity}")
    urx_service.movel(coordinates, angles, acceleration, velocity)
    return ApiResponse(200, {"status": f"moved"}).to_json()


@app.route('/ur5e/config', methods=['GET'])
def get_config():
    app.logger.info('Entered GET /ur5e/config')
    velocity = urx_service.get_velocity()
    acceleration = urx_service.get_acceleration()
    return ApiResponse(200, {"velocity": velocity, "acceleration": acceleration}).to_json()


@app.route('/ur5e/config', methods=['POST'])
def set_config():
    app.logger.info('Entered POST /ur5e/config')
    velocity = request.get_json()['velocity']
    acceleration = request.get_json()['acceleration']
    urx_service.set_velocity(velocity)
    urx_service.set_acceleration(acceleration)
    return ApiResponse(200, {"new_velocity": velocity, "new_acceleration": acceleration}).to_json()


if __name__ == "__main__":
    from waitress import serve

    serve(app, port=os.getenv("FLASK_PORT"))
