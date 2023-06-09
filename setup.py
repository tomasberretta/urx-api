import os

venv_path = os.path.join(os.getcwd(), "venv")

for root, dirs, files in os.walk(venv_path):
    if "robotiq_two_finger_gripper.py" in files:
        file_path = os.path.join(root, "robotiq_two_finger_gripper.py")
        with open(file_path, "r+") as file:
            content = file.read()
            start = content.find("def _get_new_urscript(self):")
            end = content.find("return urscript")
            method = content[start:end]
            method = method.replace("urscript._set_robot_activate()\n", "")
            method = method.replace("urscript._set_gripper_activate()\n", "")
            content = content[:start] + method + content[end:]
            file.seek(0)
            file.write(content)
            file.truncate()
        break
else:
    print(
        """
        File robotiq_two_finger_gripper.py not found. Must follow the instructions manually:
        1. Open the file robotiq_two_finger_gripper.py
        2. Find the method _get_new_urscript(self)
        3. Remove the lines urscript._set_robot_activate() and urscript._set_gripper_activate()
        4. Save the file""")
