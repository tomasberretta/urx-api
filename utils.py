import json
import logging


class ColorFormatter(logging.Formatter):
    # Define color codes for different log levels
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"  # Add green
    reset = "\x1b[0m"

    # Define the format for each log level
    FORMATS = {
        logging.DEBUG: grey + "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)" + reset,
        logging.INFO: green + "%(asctime)s - %(name)s - %(levelname)s - %(message)s " + reset,
        logging.WARNING: yellow + "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)" + reset,
        logging.ERROR: red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)" + reset,
        logging.CRITICAL: bold_red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)" + reset
    }

    # Override the format method to use the custom format
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger(logging.Logger):
    def __init__(self, name):
        # Call the parent constructor
        super().__init__(name)

        # Create a color formatter
        color_formatter = ColorFormatter()

        # Create a stream handler for the console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(color_formatter)

        # Add the handler to the logger
        self.addHandler(console_handler)

    def info(self, message, **kwargs):
        # Use the logging method instead of print
        super().info(msg=message)

    def error(self, message, **kwargs):
        # Use the logging method instead of print
        super().error(msg=message)

    def warning(self, message, **kwargs):
        # Use the logging method instead of print
        super().warning(msg=message)

    def debug(self, message, **kwargs):
        # Use the logging method instead of print
        super().debug(message)


class FlaskLogger(Logger):
    def __init__(self, app, name):
        self.name = name
        super().__init__(name)
        self._app = app

    def info(self, message, **kwargs):
        self._app.logger.info(message)

    def error(self, message, **kwargs):
        self._app.logger.error(message)

    def warning(self, message, **kwargs):
        self._app.logger.warning(message)

    def debug(self, message, **kwargs):
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
