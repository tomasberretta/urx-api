# URX API Server 
This server is a Python application that uses Flask as a web framework to create an API for controlling a UR5e robot. The API allows users to send commands to the robot and receive feedback. The server relies on the urx library, which provides a Python interface for the URScript language that the robot understands.

Additionally, the server has a functionality of passively observing the data sent between the robot and the REST server with a Proxy and another Socket Server. This works as follows: The REST server connects to the Proxy instead of the robot directly, and with every communication that is sent between them, the Proxy sends a message to the Socket Server to allow real-time observability. This way, users can monitor the robot’s status and actions without interfering with its operation.

## Prerequisites
- Python 3.8.0
  - _**Note**: Python 3.8.0 is required because of the urx library. For proper operation it is not possible to use a different version of Python._
- pip 20.2.4
- If going to use Proxy:
  - For Windows: Ncap 1.75 (https://npcap.com/#download)
  - For Linux: libpcap-dev (`sudo apt-get install libpcap-dev`)
  - For Mac: libpcap (`brew install libpcap`)

## Installation
```bash
pip install -r requirements.txt
python setup.py 
```
## Environment variables
There are 10 environment variables that need to be set:
- FLASK_HOST
- FLASK_PORT
- URX_HOST
- URX_PORT
- BOT_NAME
- PROXY
- PROXY_HOST
- PROXY_PORT
- WEBSOCKET_HOST
- WEBSOCKET_PORT

Their default values are on the `.env` file and are:
- FLASK_HOST = 127.0.0.1
- FLASK_PORT = 8080
- URX_HOST = 192.168.0.16
- URX_PORT = 30002
- BOT_NAME = ur5e
- PROXY=False
- PROXY_HOST=127.0.0.1
- PROXY_PORT=9090
- WEBSOCKET_HOST=127.0.0.1
- WEBSOCKET_PORT=5000

___Note:__ There is also an `ENVIRONMENT` environment variable that is used to set the environment to `dev` or `bot`. The default value is `bot`. If the value is `dev` the server will not try to connect to the robot._

## Starting venv and server

If running on Windows:

```bash
venv/Scripts/activate.bat
python start.py
```

Otherwise:
```bash
source venv/bin/activate
python start.py
```

## API
### Health check 
`/health`

This endpoint is used to check if the server is running.
```bash
curl -X GET http://<FLASK_HOST>:<FLASK_PORT>/health
```
### Health connection
`/<BOT_NAME>/health-connection`

This endpoint is used to check if the server is connected to the robot.
```bash
curl -X GET http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/health-connection
```

### Partial gripper
`/<BOT_NAME>/gripper/partial`

This endpoint is used to partially open or close the gripper.
```bash
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/gripper/partial -d '{"amount": 0.0}'
```
Body:
```json
{
    "amount": 0.0
}
```

### Open gripper
`/<BOT_NAME>/gripper/open`

This endpoint is used to open the gripper.
```bash
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/gripper/open
```

### Close gripper
`/<BOT_NAME>/gripper/close`

This endpoint is used to close the gripper.
```bash
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/gripper/close
```

### Movej
`/<BOT_NAME>/movej`

This endpoint is used to move the robot to a joint position.
```bash
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/movej -d '{"joint_positions": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,] "acceleration": 0.0, "velocity": 0.0, "pose_object" : true, "relative": false}'
```
Body:
```json
{
    "joint_positions": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "acceleration": 0.0,
    "velocity": 0.0,
    "pose_object" : true,
    "relative": false
}
```

### Movel
`/<BOT_NAME>/movel`

This endpoint is used to move the robot to a cartesian position.
```bash
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/movel -d '{"coordinates_and_angles": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,], "acceleration": 0.0, "velocity": 0.0, "pose_object" : true, "relative": false}'
```
Body:
```json
{
    "coordinates_and_angles": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "acceleration": 0.0,
    "velocity": 0.0,
    "pose_object" : true,
    "relative": false
}
```

### Movels
`/<BOT_NAME>/movels`

This endpoint is used to move the robot to a cartesian position for a series of coordinates.
```bash
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/movels -d '{"coordinates_list": [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], "acceleration": 0.0, "velocity": 0.0}'
```
Body:
```json
{
    "coordinates_list": [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    "acceleration": 0.0,
    "velocity": 0.0
}
```

### Move
`/<BOT_NAME>/move`

This endpoint is used to move the robot to a cartesian position.

```bash
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/move -d '{"direction": "up", "distance": 0.0, "acceleration": 0.0, "velocity": 0.0}'
```
Body:
```json
{
    "direction": "up",
    "distance": 0.0,
    "acceleration": 0.0,
    "velocity": 0.0
}
```
_**Note**: The direction can be any of the following: `up`, `down`, `left`, `right`, `forward`, `backward`, `roll`, `pitch`, `yaw`_



### Config
`/<BOT_NAME>/config`

This endpoint is used to get or set the configuration of the robot.
```bash
curl -X GET http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/config
```
```bash
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/config -d '{"velocity": 0.0, "acceleration": 0.0, "wait_timeout_limit": 0.0, "program_running_timeout_limit": 0., "amount_movement": 0.0, "amount_rotation": 0.0}'
```
Body:
```json
{
    "velocity": 0.0,
    "acceleration": 0.0,
    "wait_timeout_limit": 0.0,
    "program_running_timeout_limit": 0.0,
    "amount_movement": 0.0,
    "amount_rotation": 0.0
}
```

### Current pose
`/<BOT_NAME>/current-pose`

This endpoint is used to get the current pose of the robot.
```bash
curl -X GET http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/current-pose
```

### Current joint positions
`/<BOT_NAME>/current-joint-positions`

This endpoint is used to get the current joint positions of the robot.
```bash
curl -X GET http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/current-joint-positions
```

### Current tool position
`/<BOT_NAME>/current-tool-position`

This endpoint is used to get the current tool position of the robot.
```bash
curl -X GET http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/current-tool-position
```

