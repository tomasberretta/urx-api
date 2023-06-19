import os
import socket
import time
import numpy as np
import urx
import urx.urrobot
from dotenv import load_dotenv
from urx import robotiq_two_finger_gripper
from utils import Logger, get_acceleration_and_velocity_to_use, parse_movel_instruction, parse_movej_instruction

load_dotenv()

if os.getenv("PROXY") == "True":
    HOST = os.getenv("PROXY_HOST")
    PORT = int(os.getenv("PROXY_PORT"))
else:
    HOST = os.getenv("URX_HOST")
    PORT = int(os.getenv("URX_PORT"))


class UrxEService:

    def __init__(self, logger: Logger):
        self._logger = Logger() if logger is None else logger
        self._velocity = 0.05
        self._acceleration = 0.05
        self._wait_timeout_limit = 5
        self._program_running_timeout_limit = 60

    def get_connection_status(self):
        pass

    def open_gripper(self):
        pass

    def close_gripper(self):
        pass

    def partial_gripper(self, amount):
        pass

    def movej(self, joint_positions, acceleration, velocity, pose_object=True, relative=False):
        pass

    def movel(self, coordinates_and_angles, acceleration, velocity, pose_object=True, relative=False):
        pass

    def movels(self, coordinates_list, acceleration, velocity):
        pass

    def __move(self, direction, distance, acceleration, velocity):
        pass

    def up(self, acceleration, velocity, z=0.05):
        pass

    def down(self, acceleration, velocity, z=0.05):
        pass

    def left(self, acceleration, velocity, x=0.05):
        pass

    def right(self, acceleration, velocity, x=0.05):
        pass

    def forward(self, acceleration, velocity, y=0.05):
        pass

    def backward(self, acceleration, velocity, y=0.05):
        pass

    def __rotate(self, axis, angle, acceleration, velocity):
        pass

    def roll(self, acceleration, velocity, rx=np.pi / 16):
        pass

    def pitch(self, acceleration, velocity, ry=np.pi / 16):
        pass

    def yaw(self, acceleration, velocity, rz=np.pi / 16):
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
        """
           Get the connection status of the socket.

           Returns
           -------
           int
               The error indicator for the socket. 0 means no error.
       """
        self._logger.info("Getting connection status")
        return self._s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)

    def open_gripper(self):
        """
            Open the gripper fully.
        """
        self._logger.info("Opening gripper")
        self._robotiq_gripper.open_gripper()
        time.sleep(1)
        self._logger.info("Gripper opened")
        return  # TODO. return actual status of gripper

    def close_gripper(self):
        """
            Close the gripper fully.
        """
        self._logger.info("Closing gripper")
        self._robotiq_gripper.close_gripper()
        time.sleep(1)
        self._logger.info("Gripper closed")
        return  # TODO. return actual status of gripper

    def partial_gripper(self, amount):
        """
           Open or close the gripper partially to a given amount.

           Parameters
           ----------
           amount : int
               The amount to open or close the gripper. 0 for fully open, 255 for fully closed.
        """
        self._logger.info(f"Partially opening/closing gripper to {amount}")
        self._robotiq_gripper.gripper_action(amount)
        time.sleep(1)
        self._logger.info(f"Gripper partially opened/closed to {amount}")
        return  # TODO. return actual status of gripper

    def movej(self, joint_positions, acceleration, velocity, pose_object=True, relative=False):
        """
           Move to a given joint positions with a given acceleration and velocity.

           Parameters
           ----------
           joint_positions : list
               The list of joint positions to move to in radians.
           acceleration : float
               The acceleration to use for the movement in rad/s^2.
           velocity : float
               The velocity to use for the movement in rad/s.
           pose_object : bool, optional
               A flag indicating whether the joint positions are a pose object or a list. Default is True.
           relative : bool, optional
               A flag indicating whether the joint positions are relative to the current ones or absolute. Default is False.

           Returns
           -------
           list
               The new pose vector after the movement.
       """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        self._logger.info(
            f"Moving to joint positions: {joint_positions} , with acceleration: {acceleration} and velocity: {velocity}")
        encoded_instruction = parse_movej_instruction(joint_positions, acceleration, velocity, pose_object, relative)
        print(f"Encoded instruction: {encoded_instruction}")
        self._s.send(encoded_instruction)
        self.__wait_for_completion()
        self._logger.info(
            f"Moved to joint positions: {joint_positions}, with acceleration: {acceleration} and velocity: {velocity}")
        return self.get_current_pose()

    def movel(self, coordinates_and_angles, acceleration, velocity, pose_object=True, relative=False):
        """
            Move to a given coordinates and angles with a given acceleration and velocity.

            Parameters
            ----------
            coordinates_and_angles : list
                The list of coordinates and angles to move to in meters and radians.
            acceleration : float
                The acceleration to use for the movement in m/s^2 or rad/s^2.
            velocity : float
                The velocity to use for the movement in m/s or rad/s.
            pose_object : bool, optional
                A flag indicating whether the coordinates and angles are a pose object or a list. Default is True.
            relative : bool, optional
                A flag indicating whether the coordinates and angles are relative to the current ones or absolute. Default is False.

            Returns
            -------
            list
                The new pose vector after the movement.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        self._logger.info(
            f"Moving to coordinates and angles: {coordinates_and_angles}, with acceleration: {acceleration} and "
            f"velocity: {velocity}")
        encoded_instruction = parse_movel_instruction(coordinates_and_angles, acceleration, velocity, pose_object,
                                                      relative)
        self._s.send(encoded_instruction)
        self.__wait_for_completion()
        self._logger.info(
            f"Moved to coordinates and angles: {coordinates_and_angles}, with acceleration: {acceleration} and "
            f"velocity: {velocity}")
        return self.get_current_pose()

    def movels(self, coordinates_list, acceleration, velocity):
        """
            Move to a list of coordinates with a given acceleration and velocity.

            Parameters
            ----------
            coordinates_list : list
                The list of coordinates to move to in meters. Each element is a list of 6 values (x, y, z, rx, ry, rz).
            acceleration : float
                The acceleration to use for the movement in m/s^2 or rad/s^2.
            velocity : float
                The velocity to use for the movement in m/s or rad/s.

            Returns
            -------
            list
                The new pose vector after the movement.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        self._logger.info(
            f"Moving to coordinates list: {str(coordinates_list)}, with acceleration: {acceleration} and velocity: {velocity}")
        self._rob.movels(coordinates_list, acc=acceleration, vel=velocity, wait=False)
        self.__wait_for_completion()
        self._logger.info(
            f"Moved to coordinates list: {str(coordinates_list)}, with acceleration: {acceleration} and velocity: {velocity}")
        return self.get_current_pose()

    def __move(self, direction, distance, acceleration, velocity):
        """
        Move in a given direction by a given distance.

        Parameters
        ----------
        direction : int
            The index of the pose vector that corresponds to the direction of movement.
            0 for x, 1 for y, 2 for z, 3 for rx, 4 for ry, 5 for rz.
        distance : float
            The distance to move in meters or radians.
        acceleration : float
            The acceleration to use for the movement in m/s^2 or rad/s^2.
        velocity : float
            The velocity to use for the movement in m/s or rad/s.

        Returns
        -------
        list
            The new pose vector after the movement.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        p = self.get_current_pose()
        p[direction] += distance
        return self.movel(p, acceleration, velocity)

    def up(self, acceleration, velocity, z=0.05):
        """
        Move up in csys z.

        Parameters
        ----------
        acceleration : float, optional
            The acceleration to use for the movement in m/s^2. Default is self._acceleration.
        velocity : float, optional
            The velocity to use for the movement in m/s. Default is self._velocity.
        z : float, optional
            The distance to move up in meters. Default is 0.05.

        Returns
        -------
        list
            The new pose vector after the movement.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        return self.__move(2, z, acceleration, velocity)

    def down(self, acceleration, velocity, z=0.05):
        """
        Move down in csys z.

        Parameters
        ----------
        acceleration : float, optional
            The acceleration to use for the movement in m/s^2. Default is self._acceleration.
        velocity : float, optional
            The velocity to use for the movement in m/s. Default is self._velocity.
        z : float, optional
            The distance to move down in meters. Default is 0.05.

        Returns
        -------
        list
            The new pose vector after the movement.
         """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        return self.__move(2, -z, acceleration, velocity)

    def left(self, acceleration, velocity, x=0.05):
        """
        Move left in csys x.

        Parameters
        ----------
        acceleration : float, optional
            The acceleration to use for the movement in m/s^2. Default is self._acceleration.
        velocity : float, optional
            The velocity to use for the movement in m/s. Default is self._velocity.
        x : float, optional
            The distance to move left in meters. Default is 0.05.

        Returns
        -------
        list
            The new pose vector after the movement.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        return self.__move(0, -x, acceleration, velocity)

    def right(self, acceleration, velocity, x=0.05):
        """
        Move right in csys x.

        Parameters
        ----------
        acceleration : float, optional
            The acceleration to use for the movement in m/s^2. Default is self._acceleration.
        velocity : float, optional
            The velocity to use for the movement in m/s. Default is self._velocity.
        x : float, optional
            The distance to move right in meters. Default is 0.05.

        Returns
        -------
        list
            The new pose vector after the movement.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        return self.__move(0, x, acceleration, velocity)

    def forward(self, acceleration, velocity, y=0.05):
        """
        Move forward in csys y.

        Parameters
        ----------
        acceleration : float, optional
            The acceleration to use for the movement in m/s^2. Default is self._acceleration.
        velocity : float, optional
            The velocity to use for the movement in m/s. Default is self._velocity.
        y : float, optional
            The distance to move forward in meters. Default is 0.05.

        Returns
        -------
        list
            The new pose vector after the movement.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        return self.__move(1, y, acceleration, velocity)

    def backward(self, acceleration, velocity, y=0.05):
        """
        Move backward in csys y.

        Parameters
        ----------
        acceleration : float, optional
            The acceleration to use for the movement in m/s^2. Default is self._acceleration.
        velocity : float, optional
            The velocity to use for the movement in m/s. Default is self._velocity.
        y : float, optional
            The distance to move backward in meters. Default is 0.05.

        Returns
        -------
        list
            The new pose vector after the movement.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        return self.__move(1, -y, acceleration, velocity)

    def __rotate(self, axis, angle, acceleration, velocity):
        """
        Rotate around a given axis by a given angle.

        Parameters
        ----------
        axis : int
            The index of the pose vector that corresponds to the axis of rotation.
            0 for x, 1 for y, 2 for z, 3 for rx, 4 for ry, 5 for rz.
        angle : float
            The angle to rotate in radians.
        acceleration : float
            The acceleration to use for the rotation in rad/s^2.
        velocity : float
            The velocity to use for the rotation in rad/s.

        Returns
        -------
        list
            The new pose vector after the rotation.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        p = self.get_current_pose()
        p[axis] += angle
        return self.movel(p, acceleration, velocity)

    def roll(self, acceleration, velocity, rx=np.pi / 16):
        """
        Rotate around csys x axis.

        Parameters
        ----------
        acceleration : float, optional
            The acceleration to use for the rotation in rad/s^2. Default is self._acceleration.
        velocity : float, optional
            The velocity to use for the rotation in rad/s. Default is self._velocity.
        rx : float, optional
            The angle to rotate around x axis in radians. Default is pi/16.

        Returns
        -------
        list
            The new pose vector after the rotation.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        return self.__rotate(3, rx, acceleration, velocity)

    def pitch(self, acceleration, velocity, ry=np.pi / 16):
        """
        Rotate around csys y axis.

        Parameters
        ----------
        acceleration : float, optional
            The acceleration to use for the rotation in rad/s^2. Default is self._acceleration.
        velocity : float, optional
            The velocity to use for the rotation in rad/s. Default is self._velocity.
        ry : float, optional
            The angle to rotate around y axis in radians. Default is pi/16.

        Returns
        -------
        list
            The new pose vector after the rotation.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        return self.__rotate(4, ry, acceleration, velocity)

    def yaw(self, acceleration, velocity, rz=np.pi / 16):
        """
        Rotate around csys z axis.

        Parameters
        ----------
        acceleration : float, optional
            The acceleration to use for the rotation in rad/s^2. Default is self._acceleration.
        velocity : float, optional
            The velocity to use for the rotation in rad/s. Default is self._velocity.
        rz : float, optional
            The angle to rotate around z axis in radians. Default is pi/16.

        Returns
        -------
        list
            The new pose vector after the rotation.
        """
        acceleration, velocity = get_acceleration_and_velocity_to_use(acceleration, velocity, self._acceleration,
                                                                      self._velocity)
        return self.__rotate(5, rz, acceleration, velocity)

    def set_velocity(self, velocity):
        """
            Set the velocity for the robot movements.

            Parameters
            ----------
            velocity : float
                The velocity to set in m/s or rad/s.

            Returns
            -------
            float
                The old velocity before setting the new one.
        """
        old_velocity = self._velocity
        self._logger.info(f"Setting velocity from {old_velocity} to {velocity}")
        self._velocity = velocity
        self._logger.info(f"Set velocity from {old_velocity} to {velocity}")
        return old_velocity

    def set_acceleration(self, acceleration):
        """
            Set the acceleration for the robot movements.

            Parameters
            ----------
            acceleration : float
                The acceleration to set in m/s^2 or rad/s^2.

            Returns
            -------
            float
                The old acceleration before setting the new one.
        """
        old_acceleration = self._acceleration
        self._logger.info(f"Setting acceleration from {old_acceleration} to {acceleration}")
        self._acceleration = acceleration
        self._logger.info(f"Set acceleration from {old_acceleration} to {acceleration}")
        return old_acceleration

    def set_wait_timeout_limit(self, wait_timeout_limit):
        """
            Set the wait timeout limit for the robot movements.

            Parameters
            ----------
            wait_timeout_limit : float
                The wait timeout limit to set in seconds.

            Returns
            -------
            float
                The old wait timeout limit before setting the new one.
        """
        old_wait_timeout_limit = self._wait_timeout_limit
        self._logger.info(f"Setting wait timeout limit from {old_wait_timeout_limit} to {wait_timeout_limit}")
        self._wait_timeout_limit = wait_timeout_limit
        self._logger.info(f"Set wait timeout limit from {old_wait_timeout_limit} to {wait_timeout_limit}")
        return old_wait_timeout_limit

    def set_program_running_timeout_limit(self, program_running_timeout_limit):
        """
            Set the program running timeout limit for the robot movements.

            Parameters
            ----------
            program_running_timeout_limit : float
                The program running timeout limit to set in seconds.

            Returns
            -------
            float
                The old program running timeout limit before setting the new one.
        """
        old_program_running_timeout_limit = self._program_running_timeout_limit
        self._logger.info(
            f"Setting program running timeout limit from {old_program_running_timeout_limit} to {program_running_timeout_limit}")
        self._program_running_timeout_limit = program_running_timeout_limit
        self._logger.info(
            f"Set program running timeout limit from {old_program_running_timeout_limit} to {program_running_timeout_limit}")
        return old_program_running_timeout_limit

    def get_velocity(self):
        """
            Get the velocity for the robot movements.

            Returns
            -------
            float
                The velocity in m/s or rad/s.
        """
        self._logger.info(f"Getting velocity: {self._velocity}")
        return self._velocity

    def get_acceleration(self):
        """
            Get the acceleration for the robot movements.

            Returns
            -------
            float
                The acceleration in m/s^2 or rad/s^2.
        """
        self._logger.info(f"Getting acceleration: {self._acceleration}")
        return self._acceleration

    def get_wait_timeout_limit(self):
        """
            Get the wait timeout limit for the robot movements.

            Returns
            -------
            float
                The wait timeout limit in seconds.
        """
        self._logger.info(f"Getting wait timeout limit: {self._wait_timeout_limit}")
        return self._wait_timeout_limit

    def get_program_running_timeout_limit(self):
        """
            Get the program running timeout limit for the robot movements.

            Returns
            -------
            float
                The program running timeout limit in seconds.
        """
        self._logger.info(f"Getting program running timeout limit: {self._program_running_timeout_limit}")
        return self._program_running_timeout_limit

    def get_current_pose(self):
        """
        Get the current pose of the robot.

        Returns
            -------
            list
                The current pose of the robot.
        """
        self._logger.info(f"Getting current pose")
        coordinates_and_angles = self._rob.getl()
        self._logger.info(f"Got current pose: {coordinates_and_angles}")
        return coordinates_and_angles

    def get_current_joint_positions(self):
        """
        Get the current joint positions of the robot.

        Returns
            -------
            list
                The current joint positions of the robot.
        """
        self._logger.info(f"Getting current joint positions")
        joint_positions = self._rob.getj()
        self._logger.info(f"Got current joint positions: {joint_positions}")
        return joint_positions

    def get_current_tool_position(self):
        """
        Get the current tool position of the robot.

        Returns
            -------
            list
                The current tool position of the robot.
        """
        self._logger.info(f"Getting current tool position")
        tool_position_vector = self._rob.get_pos()
        tool_position = [tool_position_vector.x, tool_position_vector.y, tool_position_vector.z]
        self._logger.info(f"Got current tool position: {tool_position}")
        return tool_position

    def __start_bot(self):
        """
           Start the robot and the gripper and connect to the socket.
       """
        self._rob = urx.Robot(HOST)
        self._robotiq_gripper = robotiq_two_finger_gripper.Robotiq_Two_Finger_Gripper(self._rob)
        self._logger.info(f'Established IP to: {HOST}')
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._logger.info(f'Connecting to IP: {HOST} and PORT: {PORT} via socket')
        self._s.connect((HOST, PORT))
        time.sleep(0.5)
        self._logger.info(f'Connected to IP: {HOST} and PORT: {PORT} via socket')

    def __stop_bot(self):
        """
            Stop the robot and the gripper and close the socket.
        """
        self._logger.info(f"Stopping robot")
        self._rob.close()
        self._s.close()
        self._logger.info(f"Stopped robot")

    def reset(self, emergency_stopped=False):
        """
           Reset the robot and the gripper and reconnect to the socket.

           Parameters
           ----------
           emergency_stopped : bool, optional
               A flag indicating whether the robot was emergency stopped. Default is False.
       """
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
        """
            Wait for the robot program to start and complete.

            Raises
            ------
            RuntimeError
                If the program does not start or complete within the timeout limits.
        """
        self._logger.info("Waiting for program to start")
        waiting_start_time = time.time()
        while not self._rob.is_program_running():
            time.sleep(0.1)
            if time.time() - waiting_start_time > self._wait_timeout_limit:
                raise RuntimeError("Timeout waiting for program to start")
        else:
            start_time = time.time()
            self._logger.info("Waiting for program to complete")
        while self._rob.is_program_running():
            if time.time() - start_time > self._program_running_timeout_limit:
                raise RuntimeError("Timeout waiting for program to complete")


class MockUrxEService(UrxEService):

    def __init__(self):
        super().__init__(logger=Logger())
        self.__start_bot()

    def get_connection_status(self):
        return 0

    def open_gripper(self):
        return "Gripper opened"

    def close_gripper(self):
        return "Gripper closed"

    def partial_gripper(self, amount):
        return f"Gripper partially opened/closed to {amount}"

    def movej(self, joint_positions, acceleration, velocity, pose_object=True, relative=False):
        self._logger.info(
            f"Moving to joint positions: {joint_positions}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}")
        return joint_positions

    def movel(self, coordinates_and_angles, acceleration, velocity, pose_object=True, relative=False):
        self._logger.info(
            f"Moving to coordinates and angles: {coordinates_and_angles}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}")
        return coordinates_and_angles

    def movels(self, coordinates_list, acceleration, velocity):
        self._logger.info(
            f"Moving to coordinates and angles: {coordinates_list}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}")
        return coordinates_list

    def __move(self, direction, distance, acceleration, velocity):
        self._logger.info(
            f"Moving {direction} by {distance}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}")
        return [0, 0, 0, 0, 0, 0]

    def up(self, acceleration, velocity, z=0.05):
        return self.__move(2, z, acceleration, velocity)

    def down(self, acceleration, velocity, z=0.05):
        return self.__move(2, -z, acceleration, velocity)

    def left(self, acceleration, velocity, x=0.05):
        return self.__move(0, -x, acceleration, velocity)

    def right(self, acceleration, velocity, x=0.05):
        return self.__move(0, x, acceleration, velocity)

    def forward(self, acceleration, velocity, y=0.05):
        return self.__move(1, y, acceleration, velocity)

    def backward(self, acceleration, velocity, y=0.05):
        return self.__move(1, -y, acceleration, velocity)

    def __rotate(self, axis, angle, acceleration, velocity):
        self._logger.info(
            f"Rotating around {axis} by {angle}, with acceleration: {self._acceleration if acceleration is None else acceleration} and velocity: {self._velocity if velocity is None else velocity}")
        return [0, 0, 0, 0, 0, 0]

    def roll(self, acceleration, velocity, rx=np.pi / 16):
        return self.__rotate(0, rx, acceleration, velocity)

    def pitch(self, acceleration, velocity, ry=np.pi / 16):
        return self.__rotate(1, ry, acceleration, velocity)

    def yaw(self, acceleration, velocity, rz=np.pi / 16):
        return self.__rotate(2, rz, acceleration, velocity)

    def set_velocity(self, velocity):
        self._logger.info(f"Setting velocity to: {velocity}")
        old_velocity = self._velocity
        self._velocity = velocity
        return old_velocity

    def set_acceleration(self, acceleration):
        self._logger.info(f"Setting acceleration to: {acceleration}")
        old_acceleration = self._acceleration
        self._acceleration = acceleration
        return old_acceleration

    def set_wait_timeout_limit(self, wait_timeout_limit):
        self._logger.info(f"Setting wait timeout limit to: {wait_timeout_limit}")
        old_wait_timeout_limit = self._wait_timeout_limit
        self._wait_timeout_limit = wait_timeout_limit
        return old_wait_timeout_limit

    def set_program_running_timeout_limit(self, program_running_timeout_limit):
        self._logger.info(f"Setting program running timeout limit to: {program_running_timeout_limit}")
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
