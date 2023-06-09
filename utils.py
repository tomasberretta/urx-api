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


def parse_move_instruction(movement_type, coordinates, angles, acceleration, velocity, default_acceleration,
                           default_velocity):
    vector = coordinates + angles
    acceleration = default_acceleration if acceleration is None else acceleration
    velocity = default_velocity if velocity is None else velocity
    instruction = f"move{movement_type}(p{str(vector)}, {acceleration}, {velocity})\n"
    encoded_instruction = instruction.encode("utf-8")
    return encoded_instruction


def validate_json_structure(request):
    if not request.is_json:
        raise AttributeError("Invalid body, must be a JSON")
    else:
        try:
            request.json
        except Exception:
            raise AttributeError("Invalid body, must be a JSON")
