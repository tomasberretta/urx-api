# urx-api
URx REST API

## Installation and run setup.sh
```bash
pip install -r requirements.txt
python setup.py 
```
## Environment variables
There are 4 environment variables that need to be set:
- FLASK_HOST
- FLASK_PORT
- URX_HOST
- URX_PORT
- BOT_NAME

Their default values are on the `.env` file and are:
- FLASK_HOST = 127.0.0.1
- FLASK_PORT = 8080
- URX_HOST = 192.168.0.16
- URX_PORT = 30002
- BOT_NAME = ur5e

___Note:__ There is also a `ENVIRONMENT` environment variable that is used to set the environment to `dev` or `bot`. The default value is `bot`. If the value is `dev` the server will not try to connect to the robot._

## Starting venv and server

If windows:

```bash
venv/Scripts/activate.bat
python main.py
```

Otherwise:
```bash
source venv/bin/activate
python main.py
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
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/movej -d '{"coordinates": [0.0, 0.0, 0.0], angles": [0.0, 0.0, 0.0,] "acceleration": 0.0, "velocity": 0.0}'
```
Body:
```json
{
    "coordinates": [0.0, 0.0, 0.0],
    "angles": [0.0, 0.0, 0.0],
    "acceleration": 0.0,
    "velocity": 0.0
}
```

### Movel
`/<BOT_NAME>/movel`

This endpoint is used to move the robot to a cartesian position.

```bash
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/movel -d '{"coordinates": [0.0, 0.0, 0.0], angles": [0.0, 0.0, 0.0,], "acceleration": 0.0, "velocity": 0.0}'
```
Body:
```json
{
    "coordinates": [0.0, 0.0, 0.0],
    "angles": [0.0, 0.0, 0.0],
    "acceleration": 0.0,
    "velocity": 0.0
}
```

### Config
`/<BOT_NAME>/config`

This endpoint is used to get or set the configuration of the robot.

```bash
curl -X GET http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/config
```
```bash
curl -X POST http://<FLASK_HOST>:<FLASK_PORT>/<BOT_NAME>/config -d '{"velocity": 0.0, "acceleration": 0.0, "wait_timeout_limit": 0.0, "program_running_timeout_limit": 0.0}'
```
Body:
```json
{
    "velocity": 0.0,
    "acceleration": 0.0,
    "wait_timeout_limit": 0.0,
    "program_running_timeout_limit": 0.0
}
```

