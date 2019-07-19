import json


class Element(object):
    def __init__(self, title, image_url=None, subtitle=None, default_action=None, buttons=None):
        if not title:
            raise ValueError("Title must be specified")
        else:
            self.title = title
        if image_url:
            self.image_url = image_url
        if subtitle:
            self.subtitle = subtitle
        if default_action:
            self.default_action = default_action
        if buttons:
            self.buttons = buttons
            if len(self.buttons) > 3:
                raise ValueError("Element support only 3 buttons")

    def to_json(self):
        return json.dumps(self, default=lambda i: i.__dict__)


class OpenGraphElement(object):
    def __init__(self, url, buttons):
        self.url = url
        self.buttons = buttons


class MediaElement(object):
    def __init__(self, media_type, attachment_id, url, buttons):
        self.media_type = media_type
        if attachment_id and url:
            raise ValueError("Only one of the attachment_id or url must be specified")
        elif not attachment_id and not url:
            raise ValueError("attachment_id or url must be specified")
        elif attachment_id:
            self.attachment_id = attachment_id
        else:
            self.url = url
        self.buttons = buttons
        if len(self.buttons) > 1:
            raise ValueError("MediaElement support only 1 buttons")
