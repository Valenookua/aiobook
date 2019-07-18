import json


class QuickReply(object):
    def __init__(self, type="text", title=None, payload=None, image_url=None):
        if type != "text" or type != "user_phone_number" or type != "user_email":
            raise ValueError("type must be \"text\", \"user_phone_number\" or \"user_email\"")
        else:
            self.type = type
            if type == "text":
                self.title = title
                self.payload = payload
                self.image_url = image_url

    def to_json(self):
        return json.dumps(self, default=lambda i: i.__dict__)

