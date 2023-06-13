import os
import urx
import time
import socket
from utils import parse_move_instruction, Logger, parse_translate_instruction, get_acceleration_and_velocity_to_use
from dotenv import load_dotenv
from urx import robotiq_two_finger_gripper
import json

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

    def movej(self, joint_positions, acceleration, velocity):
        pass

    def movel(self, coordinates, angles, acceleration, velocity):
        pass

    def translate(self, coordinates, acceleration, velocity):
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

    def get_position(self):
        pass

    def get_current_pose(self):
        pass

    def get_current_joint_positions(self):
        pass

    def get_current_tool_position(self):
        pass

    def __start_bot(self):
        pass

    def __stop_bot(self):
        pass

    def reset(self):
        pass

    def __wait_for_completion(self):
        pass


class DefaultUrxEService(UrxEService):

    def __init__(self, logger: Logger):
        super().__init__(logger)
        self.__start_bot()

    def get_connection_status(self):
        self._logger.info("Getting connection status")
        return self._s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)

    def open_gripper(self):
        self._logger.info("Opening gripper")
        self._robotiq_gripper.open_gripper()
        time.sleep(2)
        self._logger.info("Gripper opened")
        return  # TODO. return actual status of gripper

    def close_gripper(self):
        self._logger.info("Closing gripper")
        self._robotiq_gripper.close_gripper()
        time.sleep(2)
        self._logger.info("Gripper closed")
        return  # TODO. return actual status of gripper

    def partial_gripper(self, amount):
        self._logger.info(f"Partially opening/closing gripper to {amount}")
        self._robotiq_gripper.gripper_action(amount)
        time.sleep(2)
        self._logger.info(f"Gripper partially opened/closed to {amount}")
        return  # TODO. return actual status of gripper

    def movej(self, joint_positions, acceleration, velocity):
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        self._logger.info(
            f"Moving to joint positions: {joint_positions} , with acceleration: {acceleration} and velocity: {velocity}")
        encoded_instruction = parse_move_instruction("j", joint_positions, [], acceleration, velocity)
        self._s.send(encoded_instruction)
        self.__wait_for_completion()
        self._logger.info(
            f"Moved to joint positions: {joint_positions}, with acceleration: {acceleration} and velocity: {velocity}")
        return  # TODO. return actual coordinates and angles of the robot

    def movel(self, coordinates, angles, acceleration, velocity):
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        self._logger.info(
            f"Moving to coordinates: {coordinates} and angles: {angles}, with acceleration: {acceleration} and velocity: {velocity}")
        encoded_instruction = parse_move_instruction("l", coordinates, angles, acceleration, velocity)

        self._s.send(encoded_instruction)
        self.__wait_for_completion()
        self._logger.info(
            f"Moved to coordinates: {coordinates} and angles: {angles}, with acceleration: {acceleration} and velocity: {velocity}")
        return  # TODO. return actual coordinates and angles of the robot

    def translate(self, coordinates, acceleration, velocity):
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        self._logger.info(
            f"Moving to coordinates: {coordinates}, with acceleration: {acceleration} and velocity: {velocity}")
        encoded_instruction = parse_translate_instruction(coordinates, acceleration, velocity)

        self._s.send(encoded_instruction)
        self.__wait_for_completion()
        self._logger.info(
            f"Moved to coordinates: {coordinates}, with acceleration: {acceleration} and velocity: {velocity}")
        return  # TODO. return actual coordinates and angles of the robot

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

    def get_position(self):
        data = self._s.recv(1024)
        if not data:
            return
        position = data.decode().split(",")[1:7]
        position = data.decode().split(",")[1:7]
        position_dict = {"x": position[0], "y": position[1], "z": position[2], "rx": position[3], "ry": position[4],
                         "rz": position[5]}
        position_json = json.dumps(position_dict)
        return position_json

    def get_current_pose(self):
        self._logger.info(f"Getting current pose")
        coordinates_and_angles = self._rob.getl()
        self._logger.info(f"Got current pose: {coordinates_and_angles}")
        return coordinates_and_angles

    def get_current_joint_positions(self):
        self._logger.info(f"Getting current joint positions")
        joint_positions = self._rob.getj()
        self._logger.info(f"Got current joint positions: {joint_positions}")
        return joint_positions

    def get_current_tool_position(self):
        self._logger.info(f"Getting current tool position")
        tool_position = self._rob.get_pos()
        self._logger.info(f"Got current tool position: {tool_position}")
        return tool_position

    def __start_bot(self):
        self._rob = urx.Robot(HOST)
        self._robotiq_gripper = robotiq_two_finger_gripper.Robotiq_Two_Finger_Gripper(self._rob)
        self._logger.info(f'Established IP to: {HOST}')
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._logger.info(f'Connecting to IP: {HOST} and PORT: {PORT} via socket')
        self._s.connect((HOST, PORT))
        time.sleep(0.5)
        self._logger.info(f'Connected to IP: {HOST} and PORT: {PORT} via socket')

    def __stop_bot(self):
        self._logger.info(f"Stopping robot")
        self._rob.close()
        self._s.close()
        self._logger.info(f"Stopped robot")

    def reset(self, emergency_stopped=False):
        self._logger.info(f"Resetting robot")
        if emergency_stopped:
            self._rob.secmon.close()
        self.__stop_bot()
        wait_time = 5
        self._logger.info(f"Waiting for {wait_time} seconds to reconnect to the robot")
        time.sleep(wait_time)
        self.__start_bot()
        self._logger.info(f"Reset robot")

    def __wait_for_completion(self):
        self._logger.info("Waiting for program to start")
        waiting_start_time = time.time()
        while not self._rob.is_program_running():
            time.sleep(0.1)
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

    def movej(self, joint_positions, acceleration, velocity):
        return f"Moved to joint positions: {joint_positions}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}"

    def movel(self, coordinates, angles, acceleration, velocity):
        return f"Moved to coordinates: {coordinates} and angles: {angles}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}"

    def translate(self, coordinates, acceleration, velocity):
        return f"Moved to coordinates: {coordinates}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}"

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

    def get_current_pose(self):
        return [0, 0, 0, 0, 0, 0]

    def get_current_joint_positions(self):
        return [0, 0, 0, 0, 0, 0]

    def get_current_tool_position(self):
        return [0, 0, 0]

    def __start_bot(self):
        return "Started bot"

    def __stop_bot(self):
        return "Stopped bot"

    def reset(self):
        return "Reset bot"

    def __wait_for_completion(self):
        return "Waited for completion"
