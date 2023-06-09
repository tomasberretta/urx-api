import os
import urx
import time
import socket
from utils import parse_move_instruction, Logger
from dotenv import load_dotenv
from urx import robotiq_two_finger_gripper

load_dotenv()
HOST = os.getenv("URX_HOST")
PORT = os.getenv("URX_PORT")


class UrxEService:

    def __init__(self, logger: Logger):
        self._logger = logger
        self._velocity = 0.05
        self._acceleration = 0.05
        self._wait_timeout_limit = 5
        self._program_running_timeout_limit = 30

    def get_connection_status(self):
        pass

    def open_gripper(self):
        pass

    def close_gripper(self):
        pass

    def partial_gripper(self, amount):
        pass

    def movej(self, coordinates, angles, acceleration, velocity):
        pass

    def movel(self, coordinates, angles, acceleration, velocity):
        pass

    def set_velocity(self, velocity):
        pass

    def set_acceleration(self, acceleration):
        pass

    def set_wait_timeout_limit(self, wait_timeout_limit):
        pass

    def set_program_running_timeout_limit(self, program_running_timeout_limit):
        pass

    def get_velocity(self):
        pass

    def get_acceleration(self):
        pass

    def get_wait_timeout_limit(self):
        pass

    def get_program_running_timeout_limit(self):
        pass

    def __wait_for_completion(self):
        pass


class DefaultUrxEService(UrxEService):

    def __init__(self, logger: Logger):
        super().__init__(logger)
        self._rob = urx.Robot(HOST)
        self._robotiq_gripper = robotiq_two_finger_gripper.Robotiq_Two_Finger_Gripper(self._rob)
        self._logger.info(f'Established IP to: {HOST}')
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._logger.info(f'Connecting to IP: {HOST} and PORT: {PORT} via socket')
        self._s.connect((HOST, PORT))
        time.sleep(0.5)
        self._logger.info(f'Connected to IP: {HOST} and PORT: {PORT} via socket')

    def get_connection_status(self):
        self._logger.info("Getting connection status")
        return self._s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)

    def open_gripper(self):
        self._logger.info("Opening gripper")
        self._robotiq_gripper.open_gripper()
        time.sleep(2)
        self._logger.info("Gripper opened")
        return # TODO. return actual status of gripper

    def close_gripper(self):
        self._logger.info("Closing gripper")
        self._robotiq_gripper.close_gripper()
        time.sleep(2)
        self._logger.info("Gripper closed")
        return # TODO. return actual status of gripper

    def partial_gripper(self, amount):
        self._logger.info(f"Partially opening/closing gripper to {amount}")
        self._robotiq_gripper.gripper_action(amount)
        time.sleep(2)
        self._logger.info(f"Gripper partially opened/closed to {amount}")
        return # TODO. return actual status of gripper

    def movej(self, coordinates, angles, acceleration, velocity):
        self._logger.info(
            f"Moving to coordinates: {coordinates} and angles: {angles}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}")
        encoded_instruction = parse_move_instruction("j", coordinates, angles, acceleration, velocity,
                                                     self._acceleration, self._velocity)
        self._s.send(encoded_instruction)
        self.__wait_for_completion()
        self._logger.info(
            f"Moved to coordinates: {coordinates} and angles: {angles}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}")
        return # TODO. return actual coordinates and angles of the robot

    def movel(self, coordinates, angles, acceleration, velocity):
        self._logger.info(
            f"Moving to coordinates: {coordinates} and angles: {angles}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}")
        encoded_instruction = parse_move_instruction("l", coordinates, angles, acceleration, velocity,
                                                     self._acceleration, self._velocity)

        self._s.send(encoded_instruction)
        self.__wait_for_completion()
        self._logger.info(
            f"Moved to coordinates: {coordinates} and angles: {angles}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}")
        return # TODO. return actual coordinates and angles of the robot

    def set_velocity(self, velocity):
        old_velocity = self._velocity
        self._logger.info(f"Setting velocity from {old_velocity} to {velocity}")
        self._velocity = velocity
        self._logger.info(f"Set velocity from {old_velocity} to {velocity}")
        return old_velocity

    def set_acceleration(self, acceleration):
        old_acceleration = self._acceleration
        self._logger.info(f"Setting acceleration from {old_acceleration} to {acceleration}")
        self._acceleration = acceleration
        self._logger.info(f"Set acceleration from {old_acceleration} to {acceleration}")
        return old_acceleration

    def set_wait_timeout_limit(self, wait_timeout_limit):
        old_wait_timeout_limit = self._wait_timeout_limit
        self._logger.info(f"Setting wait timeout limit from {old_wait_timeout_limit} to {wait_timeout_limit}")
        self._wait_timeout_limit = wait_timeout_limit
        self._logger.info(f"Set wait timeout limit from {old_wait_timeout_limit} to {wait_timeout_limit}")
        return old_wait_timeout_limit

    def set_program_running_timeout_limit(self, program_running_timeout_limit):
        old_program_running_timeout_limit = self._program_running_timeout_limit
        self._logger.info(
            f"Setting program running timeout limit from {old_program_running_timeout_limit} to {program_running_timeout_limit}")
        self._program_running_timeout_limit = program_running_timeout_limit
        self._logger.info(
            f"Set program running timeout limit from {old_program_running_timeout_limit} to {program_running_timeout_limit}")
        return old_program_running_timeout_limit

    def get_velocity(self):
        self._logger.info(f"Getting velocity: {self._velocity}")
        return self._velocity

    def get_acceleration(self):
        self._logger.info(f"Getting acceleration: {self._acceleration}")
        return self._acceleration

    def get_wait_timeout_limit(self):
        self._logger.info(f"Getting wait timeout limit: {self._wait_timeout_limit}")
        return self._wait_timeout_limit

    def get_program_running_timeout_limit(self):
        self._logger.info(f"Getting program running timeout limit: {self._program_running_timeout_limit}")
        return self._program_running_timeout_limit

    def __wait_for_completion(self):
        self._logger.info("Waiting for program to start")
        waiting_start_time = time.time()
        while not self._rob.is_program_running():
            time.sleep(0.1)  # sleep first since the information may be outdated
            if waiting_start_time - time.time() > self._wait_timeout_limit:
                raise RuntimeError("Timeout waiting for program to start")
        else:
            start_time = time.time()
            self._logger.info("Waiting for program to complete")
        while self._rob.is_program_running():
            if time.time() - start_time > self._program_running_timeout_limit:
                raise RuntimeError("Timeout waiting for program to complete")


class MockUrxEService(UrxEService):

    def get_connection_status(self):
        return 0

    def open_gripper(self):
        return "Gripper opened"

    def close_gripper(self):
        return "Gripper closed"

    def partial_gripper(self, amount):
        return f"Gripper partially opened/closed to {amount}"

    def movej(self, coordinates, angles, acceleration, velocity):
        return f"Moved to coordinates: {coordinates} and angles: {angles}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}"

    def movel(self, coordinates, angles, acceleration, velocity):
        return f"Moved to coordinates: {coordinates} and angles: {angles}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}"

    def set_velocity(self, velocity):
        old_velocity = self._velocity
        self._velocity = velocity
        return old_velocity

    def set_acceleration(self, acceleration):
        old_acceleration = self._acceleration
        self._acceleration = acceleration
        return old_acceleration

    def set_wait_timeout_limit(self, wait_timeout_limit):
        old_wait_timeout_limit = self._wait_timeout_limit
        self._wait_timeout_limit = wait_timeout_limit
        return old_wait_timeout_limit

    def set_program_running_timeout_limit(self, program_running_timeout_limit):
        old_program_running_timeout_limit = self._program_running_timeout_limit
        self._program_running_timeout_limit = program_running_timeout_limit
        return old_program_running_timeout_limit

    def get_velocity(self):
        return self._velocity

    def get_acceleration(self):
        return self._acceleration

    def get_wait_timeout_limit(self):
        return self._wait_timeout_limit

    def get_program_running_timeout_limit(self):
        return self._program_running_timeout_limit

    def __wait_for_completion(self):
        return "Waited for completion"
