import os
import subprocess
import platform
from dotenv import load_dotenv

load_dotenv()

run_env = []
to_run = []

# Get the current system name
system = platform.system()

# Activate the venv depending on the system
if system == "Windows":
    # Run the venv/Scripts/activate.bat file
    run_env.append("venv\\Scripts\\activate.bat")
else:
    # Run the source venv/bin/activate command
    run_env.append("source")
    run_env.append("venv/bin/activate")

# # Check if the environment variable PROXY is True
if os.environ.get("PROXY") == "True":
    # Run the socket_server.py file
    run_start_socket_server = []
    run_start_socket_server += run_env
    run_start_socket_server.append("&&")
    run_start_socket_server.append("python")
    run_start_socket_server.append("socket_server.py")
    to_run.append(run_start_socket_server)

    # Run the proxy_server.py file
    run_start_proxy_server = []
    run_start_proxy_server += run_env
    run_start_proxy_server.append("&&")
    run_start_proxy_server.append("python")
    run_start_proxy_server.append("proxy_server.py")
    to_run.append(run_start_proxy_server)

    # Run the main.py file
    run_start_main = []
    run_start_main += run_env
    run_start_main.append("&&")
    run_start_main.append("python")
    run_start_main.append("main.py")
    to_run.append(run_start_main)
else:
    # Run the main.py file
    run_start_main = []
    run_start_main += run_env
    run_start_main.append("&&")
    run_start_main.append("python")
    run_start_main.append("main.py")
    to_run.append(run_start_main)

# Run each element of to_run on a separated terminal depending on the system
for run in to_run:
    # Join the elements of run with spaces to form a command string
    cmd = " ".join(run)
    # Add a pause command to the end of the cmd string to keep the terminal open after the script finishes
    cmd = cmd + " & pause"

    # Check the system and use the corresponding terminal command
    if system == "Windows":
        # Use cmd to open a new console window and execute the cmd string
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
        # Use osascript to open a new terminal window and execute the cmd string
        subprocess.Popen(["osascript", "-e", f'tell application "Terminal" to do script "{cmd}"'])

        # Alternatively, you can use open to open a new terminal window and execute the cmd string
        # subprocess.Popen(["open", "-a", "Terminal.app", "--args", "-c", cmd])

    else:
        # Handle other systems or raise an error
        print(f"Unsupported system: {system}")
