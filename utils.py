import json


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


class ApiResponse:
    def __init__(self, status, body):
        self.__status = status
        self.__body = body

    def to_json(self):
        return json.dumps(self.__body), self.__status


def parse_movel_instruction(coordinates_and_angles, acceleration, velocity, pose_object, relative):
    if pose_object:
        instruction = f"movel(p{str(coordinates_and_angles)}, {acceleration}, {velocity}"
    else:
        instruction = f"movel({str(coordinates_and_angles)}, {acceleration}, {velocity}"
    if relative:
        instruction = instruction + ", relative=True)\n"
    else:
        instruction = instruction + ")\n"
    encoded_instruction = instruction.encode("utf-8")
    return encoded_instruction


def parse_movej_instruction(joint_positions, acceleration, velocity, position, relative):
    if position:
        instruction = f"movej(p{str(joint_positions)}, {acceleration}, {velocity})\n"
    else:
        instruction = f"movej({str(joint_positions)}, {acceleration}, {velocity})\n"
    if relative:
        instruction = instruction + ", relative=True)\n"
    else:
        instruction = instruction + ")\n"
    encoded_instruction = instruction.encode("utf-8")
    return encoded_instruction


def get_acceleration_and_velocity_to_use(acceleration, velocity, default_acceleration, default_velocity):
    acceleration = default_acceleration if acceleration is None else acceleration
    velocity = default_velocity if velocity is None else velocity
    return acceleration, velocity


def validate_json_structure(request):
    if not request.is_json:
        raise AttributeError("Invalid body, must be a JSON")
    else:
        try:
            request.json
        except Exception:
            raise AttributeError("Invalid body, must be a JSON")
