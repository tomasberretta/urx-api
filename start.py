import os
import subprocess
import platform
from dotenv import load_dotenv

load_dotenv()

run_env = []
to_run = []

system = platform.system()

if system == "Windows":
    run_env.append("venv\\Scripts\\activate.bat")
else:
    run_env.append("source")
    run_env.append("venv/bin/activate")

if os.environ.get("PROXY") == "True":
    run_start_socket_server = []
    run_start_socket_server += run_env
    run_start_socket_server.append("&&")
    run_start_socket_server.append("python")
    run_start_socket_server.append("socket_server.py")
    to_run.append(run_start_socket_server)

    run_start_proxy_server = []
    run_start_proxy_server += run_env
    run_start_proxy_server.append("&&")
    run_start_proxy_server.append("python")
    run_start_proxy_server.append("proxy_server.py")
    to_run.append(run_start_proxy_server)

    run_start_main = []
    run_start_main += run_env
    run_start_main.append("&&")
    run_start_main.append("python")
    run_start_main.append("main.py")
    to_run.append(run_start_main)
else:
    run_start_main = []
    run_start_main += run_env
    run_start_main.append("&&")
    run_start_main.append("python")
    run_start_main.append("main.py")
    to_run.append(run_start_main)

for run in to_run:
    cmd = " ".join(run)
    # Add a pause command to the end of the cmd string to keep the terminal open after the script finishes
    cmd = cmd + " & pause"

    if system == "Windows":
        from subprocess import CREATE_NEW_CONSOLE
        subprocess.Popen(["cmd", "/c", cmd], creationflags=CREATE_NEW_CONSOLE)

        # Alternatively, you can use start to open a new console window and execute the cmd string
        # subprocess.Popen(["start", "cmd", "/c", cmd], shell=True)

        # You can also use powershell instead of cmd if you prefer
        # subprocess.Popen(["powershell", "-Command", cmd], creationflags=CREATE_NEW_CONSOLE)

        # Or use start with powershell
        # subprocess.Popen(["start", "powershell", "-Command", cmd], shell=True)

    elif system == "Linux":
        # Use xterm to open a new terminal window and execute the cmd string
        subprocess.Popen(["xterm", "-hold", "-e", cmd])

        # Alternatively, you can use gnome-terminal to open a new terminal window and execute the cmd string
        # subprocess.Popen(["gnome-terminal", "--", "/bin/bash", "-c", cmd])

    elif system == "Darwin":
        directory = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen(["open", "-a", "Terminal.app", "--args", "-c", f"cd {directory} && {cmd}"])

    else:
        print(f"Unsupported system: {system}")
