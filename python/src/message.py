from .util import check_type
import json
from json_cpp import JsonObject, JsonList


class Message(JsonObject):

    def __init__(self, header="", body=""):
        self.header = header
        self.body = str(body)
        self._source = None

    def get_body(self, body_type=None):
        if body_type:
            check_type(body_type, type, "wrong type for body_body")
            if body_type is JsonObject or body_type is JsonList:
                return JsonObject.load(self.body)
            elif issubclass(body_type, JsonObject) or issubclass(body_type, JsonList):
                return body_type.parse(self.body)
            else:
                if body_type is str:
                    return self.body
                else:
                    return body_type(json.loads(self.body))
        else:
            return self.body

    def set_body(self, v):
        self.body = str(v)

    def reply(self, message):
        check_type(message, Message, "wrong type for message")
        if self._source:
            self._source.send(message)
            return True
        else:
            return False