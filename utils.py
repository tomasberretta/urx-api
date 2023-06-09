import json


class ApiResponse:
    def __init__(self, status, body):
        self.__status = status
        self.__body = body

    def to_json(self):
        return json.dumps(self.__body), self.__status
