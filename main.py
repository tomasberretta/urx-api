import json
import os
from logging.config import dictConfig

from dotenv import load_dotenv
from flask import Flask, request
from marshmallow import ValidationError
from waitress import serve

from schemas import PartialGripperRequestSchema, MoveRequestSchema, SetConfigRequestSchema
from urx_service import DefaultUrxEService, MockUrxEService
from utils import ApiResponse, FlaskLogger, validate_json_structure

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
logger = FlaskLogger(app)
BOT_NAME = os.getenv("BOT_NAME")
if os.getenv("ENVIRONMENT") == "dev":
    urx_service = MockUrxEService(logger=logger)
else:
    urx_service = DefaultUrxEService(logger=logger)


@app.route('/health', methods=['GET'])
def health():
    return json.loads('{"status": "ok"}'), 200


@app.route(f'/{BOT_NAME}/health-connection', methods=['GET'])
def health_check():
    status = urx_service.get_connection_status()
    if status != 0:
        return ApiResponse(500, {"status": f"Error: {status}"}).to_json()
    return ApiResponse(200, {"status": "ok"}).to_json()


@app.route(f'/{BOT_NAME}/gripper/partial', methods=['POST'])
def partial_gripper():
    try:
        validate_json_structure(request)
        data = PartialGripperRequestSchema().load(request.json)
        logger.info('Entered POST /ur5e/gripper/partial')
        amount = data['amount']
        urx_service.partial_gripper(amount=amount)
        return ApiResponse(200, {"status": f"Gripper partially moved to {amount}"}).to_json()
    except ValidationError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": f"Error: {e.messages}"}).to_json()
    except AttributeError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": str(e)}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/gripper/open', methods=['POST'])
def open_gripper():
    try:
        logger.info('Entered POST /ur5e/gripper/open')
        urx_service.open_gripper()
        return ApiResponse(200, {"status": "Gripper fully open"}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/gripper/close', methods=['POST'])
def close_gripper():
    try:
        logger.info('Entered POST /ur5e/gripper/close')
        urx_service.close_gripper()
        return ApiResponse(200, {"status": "Gripper fully closed"}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/movej', methods=['POST'])
def movej():
    try:
        validate_json_structure(request)
        data = MoveRequestSchema().load(request.json)
        logger.info('Entered POST /ur5e/movej')
        coordinates = data['coordinates']
        angles = data['angles']
        # if acceleration and velocity are not provided, send as None
        acceleration = data.get('acceleration', None)
        velocity = data.get('velocity', None)
        urx_service.movej(coordinates, angles, acceleration, velocity)
        return ApiResponse(200, {"status": f"Moved successfully"}).to_json()
    except ValidationError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": f"Error: {e.messages}"}).to_json()
    except AttributeError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": str(e)}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/movel', methods=['POST'])
def movel():
    try:
        validate_json_structure(request)
        data = MoveRequestSchema().load(request.json)
        logger.info('Entered POST /ur5e/movel')
        coordinates = data['coordinates']
        angles = data['angles']
        acceleration = data['acceleration']
        velocity = data['velocity']
        urx_service.movel(coordinates, angles, acceleration, velocity)
        return ApiResponse(200, {"status": f"Moved successfully"}).to_json()
    except ValidationError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": f"Error: {e.messages}"}).to_json()
    except AttributeError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": str(e)}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/config', methods=['GET'])
def get_config():
    try:
        logger.info('Entered GET /ur5e/config')
        velocity = urx_service.get_velocity()
        acceleration = urx_service.get_acceleration()
        wait_timeout_limit = urx_service.get_wait_timeout_limit()
        program_running_timeout_limit = urx_service.get_program_running_timeout_limit()
        return ApiResponse(200,
                           {
                               "velocity": velocity,
                               "acceleration": acceleration,
                               "wait_timeout_limit": wait_timeout_limit,
                               "program_running_timeout_limit": program_running_timeout_limit
                           }
                           ).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/config', methods=['POST'])
def set_config():
    try:
        validate_json_structure(request)
        data = SetConfigRequestSchema().load(request.json)
        logger.info('Entered POST /ur5e/config')
        velocity = data['velocity']
        acceleration = data['acceleration']
        wait_timeout_limit = data['wait_timeout_limit']
        program_running_timeout_limit = data['program_running_timeout_limit']
        old_velocity = urx_service.set_velocity(velocity)
        old_acceleration = urx_service.set_acceleration(acceleration)
        old_wait_timeout_limit = urx_service.set_wait_timeout_limit(wait_timeout_limit)
        old_program_running_timeout_limit = urx_service.set_program_running_timeout_limit(program_running_timeout_limit)
        return ApiResponse(200,
                           {
                               "old_velocity": old_velocity,
                               "old_acceleration": old_acceleration,
                               "old_wait_timeout_limit": old_wait_timeout_limit,
                               "old_program_running_timeout_limit": old_program_running_timeout_limit,
                               "new_velocity": velocity,
                               "new_acceleration": acceleration,
                               "new_wait_timeout_limit": wait_timeout_limit,
                               "new_program_running_timeout_limit": program_running_timeout_limit
                           }
                           ).to_json()
    except ValidationError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": f"Error: {e.messages}"}).to_json()
    except AttributeError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": str(e)}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


if __name__ == "__main__":
    logger.info(f"Flask server starting at {os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}")
    serve(app, host=os.getenv("FLASK_HOST"), port=os.getenv("FLASK_PORT"))
