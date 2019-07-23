import json


class Element(object):
    def __init__(self, title, image_url=None, subtitle=None, default_action=None, buttons=None):
        """
        :param title:
        :param image_url:
        :param subtitle:
        :param default_action:
        :param buttons:
        """
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
            if not isinstance(buttons, list):
                raise ValueError(f"buttons must be a list, got {type(buttons)}")
            self.buttons = buttons
            if len(self.buttons) > 3:
                raise ValueError("Element support only 3 buttons")

    def to_json(self):
        return json.dumps(self, default=lambda i: i.__dict__)


class OpenGraphElement(object):
    def __init__(self, url, buttons):
        """
        :param url:
        :param buttons:
        """
        self.url = url
        if not isinstance(buttons, list):
            raise ValueError(f"buttons must be a list, got {type(buttons)}")
        self.buttons = buttons


class MediaElement(object):
    def __init__(self, media_type, attachment_id=None, url=None, buttons=None):
        """
        :param media_type:
        :param attachment_id:
        :param url:
        :param buttons:
        """
        self.media_type = media_type
        if attachment_id and url:
            raise ValueError("Only one of the attachment_id or url must be specified")
        elif not attachment_id and not url:
            raise ValueError("attachment_id or url must be specified")
        elif attachment_id:
            self.attachment_id = attachment_id
        else:
            self.url = url
        if buttons:
            if not isinstance(buttons, list):
                raise ValueError(f"buttons must be a list, got {type(buttons)}")
            self.buttons = buttons
            if len(self.buttons) > 1:
                raise ValueError("MediaElement support only 1 buttons")
