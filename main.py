import json
import os
from logging.config import dictConfig

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS, cross_origin
from marshmallow import ValidationError
from waitress import serve

from logger import FlaskLogger, ColorFormatter
from schemas import PartialGripperRequestSchema, SetConfigRequestSchema, MoveJRequestSchema, \
    MoveLRequestSchema, MoveLSRequestSchema, MoveRequestSchema
from urx_service import DefaultUrxEService, MockUrxEService
from utils import ApiResponse, validate_json_structure

load_dotenv()

dictConfig({
    'version': 1,
    'formatters': {'color': {
        '()': ColorFormatter
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'color'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask("Flask Server")
logger = FlaskLogger(app, "Flask Server")

BOT_NAME = os.getenv("BOT_NAME")

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

try:
    if os.getenv("ENVIRONMENT") == "dev":
        urx_service = MockUrxEService()
    else:
        urx_service = DefaultUrxEService(logger=logger)
except Exception as e:
    logger.error(f"Failed to initialize UrxEService: {e}")
    exit(1)


@app.route("/")
@cross_origin()
def root_path():
    return json.loads('{"status": "ok"}'), 200


@app.route('/health', methods=['GET'])
@cross_origin()
def health():
    return json.loads('{"status": "ok"}'), 200


@app.route(f'/{BOT_NAME}/health-connection', methods=['GET'])
@cross_origin()
def health_check():
    status = urx_service.get_connection_status()
    if status != 0:
        return ApiResponse(500, {"status": f"Error: {status}"}).to_json()
    return ApiResponse(200, {"status": "ok"}).to_json()


@app.route(f'/{BOT_NAME}/gripper/partial', methods=['POST'])
@cross_origin()
def partial_gripper():
    try:
        validate_json_structure(request)
        data = PartialGripperRequestSchema().load(request.json)
        logger.info(f'Entered POST /{BOT_NAME}/gripper/partial')
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
@cross_origin()
def open_gripper():
    try:
        logger.info(f'Entered POST /{BOT_NAME}/gripper/open')
        urx_service.open_gripper()
        return ApiResponse(200, {"status": "Gripper fully open"}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/gripper/close', methods=['POST'])
@cross_origin()
def close_gripper():
    try:
        logger.info(f'Entered POST /{BOT_NAME}/gripper/close')
        urx_service.close_gripper()
        return ApiResponse(200, {"status": "Gripper fully closed"}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/movej', methods=['POST'])
@cross_origin()
def movej():
    try:
        validate_json_structure(request)
        data = MoveJRequestSchema().load(request.json)
        logger.info(f'Entered POST /{BOT_NAME}/movej')
        joint_positions = data['joint_positions']
        acceleration = data.get('acceleration', None)
        velocity = data.get('velocity', None)
        pose_object = data.get('pose_object', True)
        relative = data.get('relative', False)
        moved_to = urx_service.movej(joint_positions, acceleration, velocity, pose_object, relative)
        return ApiResponse(200, {"status": moved_to}).to_json()
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
@cross_origin()
def movel():
    try:
        validate_json_structure(request)
        data = MoveLRequestSchema().load(request.json)
        logger.info(f'Entered POST /{BOT_NAME}/movel')
        coordinates_and_angles = data['coordinates_and_angles']
        acceleration = data.get('acceleration', None)
        velocity = data.get('velocity', None)
        pose_object = data.get('pose_object', True)
        relative = data.get('relative', False)
        moved_to = urx_service.movel(coordinates_and_angles, acceleration, velocity, pose_object, relative)
        return ApiResponse(200, {"status": moved_to}).to_json()
    except ValidationError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": f"Error: {e.messages}"}).to_json()
    except AttributeError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": str(e)}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/movels', methods=['POST'])
@cross_origin()
def movels():
    try:
        validate_json_structure(request)
        data = MoveLSRequestSchema().load(request.json)
        logger.info(f'Entered POST /{BOT_NAME}/movels')
        coordinates_list = data['coordinates_list']
        acceleration = data.get('acceleration', None)
        velocity = data.get('velocity', None)
        moved_to = urx_service.movels(coordinates_list, acceleration, velocity)
        return ApiResponse(200, {"status": moved_to}).to_json()
    except ValidationError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": f"Error: {e.messages}"}).to_json()
    except AttributeError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": str(e)}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/move', methods=["POST"])
@cross_origin()
def move():
    try:
        validate_json_structure(request)
        data = MoveRequestSchema().load(request.json)
        logger.info(f'Entered POST /{BOT_NAME}/move')
        direction = data["direction"]
        distance = data.get("distance", None)
        acceleration = data.get("acceleration", None)
        velocity = data.get("velocity", None)
        moved_to = getattr(urx_service, direction)(distance, acceleration, velocity)
        return ApiResponse(200, {"status": moved_to}).to_json()
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
@cross_origin()
def get_config():
    try:
        logger.info(f'Entered GET /{BOT_NAME}/config')
        velocity = urx_service.get_velocity()
        acceleration = urx_service.get_acceleration()
        wait_timeout_limit = urx_service.get_wait_timeout_limit()
        program_running_timeout_limit = urx_service.get_program_running_timeout_limit()
        amount_movement = urx_service.get_amount_movement()
        amount_rotation = urx_service.get_amount_rotation()
        return ApiResponse(200,
                           {
                               "velocity": velocity,
                               "acceleration": acceleration,
                               "wait_timeout_limit": wait_timeout_limit,
                               "program_running_timeout_limit": program_running_timeout_limit,
                               "amount_movement": amount_movement,
                               "amount_rotation": amount_rotation
                           }
                           ).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/config', methods=['POST'])
@cross_origin()
def set_config():
    try:
        validate_json_structure(request)
        data = SetConfigRequestSchema().load(request.json)
        logger.info(f'Entered POST /{BOT_NAME}/config')
        velocity = data.get('velocity', None)
        acceleration = data.get('acceleration', None)
        wait_timeout_limit = data.get('wait_timeout_limit', None)
        program_running_timeout_limit = data.get('program_running_timeout_limit', None)
        amount_movement = data.get('amount_movement', None)
        amount_rotation = data.get('amount_rotation', None)
        response = {}

        if velocity is not None:
            old_velocity = urx_service.set_velocity(velocity)
            response["old_velocity"] = old_velocity
            response["new_velocity"] = velocity

        if acceleration is not None:
            old_acceleration = urx_service.set_acceleration(acceleration)
            response["old_acceleration"] = old_acceleration
            response["new_acceleration"] = acceleration

        if wait_timeout_limit is not None:
            old_wait_timeout_limit = urx_service.set_wait_timeout_limit(wait_timeout_limit)
            response["old_wait_timeout_limit"] = old_wait_timeout_limit
            response["new_wait_timeout_limit"] = wait_timeout_limit

        if program_running_timeout_limit is not None:
            old_program_running_timeout_limit = urx_service.set_program_running_timeout_limit(
                program_running_timeout_limit)
            response["old_program_running_timeout_limit"] = old_program_running_timeout_limit
            response["new_program_running_timeout_limit"] = program_running_timeout_limit

        if amount_movement is not None:
            old_amount_movement = urx_service.set_amount_movement(amount_movement)
            response["old_amount_movement"] = old_amount_movement
            response["new_amount_movement"] = amount_movement

        if amount_rotation is not None:
            old_amount_rotation = urx_service.set_amount_rotation(amount_rotation)
            response["old_amount_rotation"] = old_amount_rotation
            response["new_amount_rotation"] = amount_rotation

        return ApiResponse(200, response).to_json()
    except ValidationError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": f"Error: {e.messages}"}).to_json()
    except AttributeError as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(400, {"status": str(e)}).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/current-pose', methods=['GET'])
@cross_origin()
def get_current_pose():
    try:
        logger.info(f'Entered GET /{BOT_NAME}/current-pose')
        current_pose = urx_service.get_current_pose()
        return ApiResponse(200,
                           {
                               "current_pose": current_pose
                           }
                           ).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/current-joint-positions', methods=['GET'])
@cross_origin()
def get_current_joint_positions():
    try:
        logger.info(f'Entered GET /{BOT_NAME}/current-joint-positions')
        current_joint_positions = urx_service.get_current_joint_positions()
        return ApiResponse(200,
                           {
                               "current_joint_positions": current_joint_positions
                           }
                           ).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


@app.route(f'/{BOT_NAME}/current-tool-position', methods=['GET'])
@cross_origin()
def get_current_tool_position():
    try:
        logger.info(f'Entered GET /{BOT_NAME}/current-tool-position')
        current_tool_position = urx_service.get_current_tool_position()
        return ApiResponse(200,
                           {
                               "current_tool_position": current_tool_position
                           }
                           ).to_json()
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return ApiResponse(500, {"status": f"Error: {e}"}).to_json()


if __name__ == "__main__":
    logger.info(f"Flask server starting at {os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}")
    serve(app, host=os.getenv("FLASK_HOST"), port=os.getenv("FLASK_PORT"))
