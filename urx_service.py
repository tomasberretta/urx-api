HOST = "192.168.0.16"  # IP del robot
PORT = 30002

import time
import socket
from urx import robotiq_two_finger_gripper
import urx


class UrxEService:

    def __init__(self):
        self._rob = urx.Robot(HOST)
        self._robotiqgrip = robotiq_two_finger_gripper.Robotiq_Two_Finger_Gripper(self._rob)

        print("Conectando a IP: ", HOST)
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("conectando...")
        self._s.connect((HOST, PORT))
        time.sleep(0.5)
        print("Conectado con el robot")
        self._velocity = 0.05
        self._acceleration = 0.05

    def health_check(self):
        status = self._s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        return {"status": "ok" if status == 0 else "error"}

    def open_gripper(self):
        self._robotiqgrip.open_gripper()
        time.sleep(2)
        return

    def close_gripper(self):
        self._robotiqgrip.close_gripper()
        time.sleep(2)
        return

    def partial_gripper(self, amount):
        self._robotiqgrip.gripper_action(amount)
        time.sleep(2)
        return

    def movej(self, coordinates, angles, acceleration, velocity):
        vector = coordinates + angles
        acceleration = self._acceleration if acceleration is None else acceleration
        velocity = self._velocity if velocity is None else velocity
        instruction = f"movej(p{str(vector)}, {acceleration}, {velocity})\n"
        encoded_instruction = instruction.encode("utf-8")
        self._s.send(encoded_instruction)
        time.sleep(5)
        return

    def movel(self, coordinates, angles, acceleration, velocity):
        vector = coordinates + angles
        acceleration = self._acceleration if acceleration is None else acceleration
        velocity = self._velocity if velocity is None else velocity
        instruction = f"movel(p{str(vector)}, {acceleration}, {velocity})\n"
        encoded_instruction = instruction.encode("utf-8")
        self._s.send(encoded_instruction)
        return

    def set_velocity(self, velocity):
        self._velocity = velocity
        return

    def set_acceleration(self, acceleration):
        self._acceleration = acceleration
        return

    def get_velocity(self):
        return self._velocity

    def get_acceleration(self):
        return self._acceleration
