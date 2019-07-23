import json


class Recipient(object):
    def __init__(self, id_=None, phone_number=None, user_ref=None, name=None):
        if id_:
            self.id = id_
        if phone_number:
            self.phone_number = phone_number
            if name:
                self.name = name
        if user_ref:
            self.user_ref = user_ref

        if not self.id and not self.phone_number and not self.user_ref:
            raise ValueError


class Message(object):
    def __init__(self, text, attachment=None, quick_replies=None, metadata=None):
        if text:
            self.text = text
        if attachment:
            self.attachment = attachment
        if quick_replies:
            self.quick_replies = quick_replies
        if metadata:
            self.metadata = metadata


class Attachment(object):
    def __init__(self, type, payload):
        self.type = type
        self.payload = payload


class Payload(object):
    def __init__(self, messaging_type,
                 recipient: Recipient,
                 message: Message or None,
                 sender_action=None,
                 notification_type=None,
                 tag=None):
        self.recipient = recipient
        if messaging_type:
            self.messaging_type = messaging_type
        if message:
            self.message = message
        if sender_action:
            self.sender_action = sender_action
        if notification_type:
            self.notification_type = notification_type
        if tag:
            self.tag = tag

    def to_json(self):
        return json.dumps(self, default=lambda i: i.__dict__)


class PersistentMenu(object):
    def __init__(self, persistent_menu):
        self.persistent_menu = persistent_menu

    def to_json(self):
        return json.dumps(self, default=lambda i: i.__dict__)


class PersistentMenuElement(object):
    def __init__(self, call_to_actions, locale="default", composer_input_disabled=False):
        self.call_to_actions = call_to_actions
        self.locale = locale
        self.composer_input_disabled = composer_input_disabled

    def to_json(self):
        return json.dumps(self, default=lambda i: i.__dict__)
