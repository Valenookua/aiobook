import json


class Event(object):
    def __init__(self, sender=None, recipient=None, timestamp=None, **kwargs):
        self.raw = kwargs
        self.sender = sender if sender else {}
        self.recipient = recipient if recipient else {}
        self.timestamp = timestamp

    def __str__(self):
        return json.dumps(self.__class__.__name__)

    @classmethod
    def from_json(cls, json_dict):
        return cls(**json_dict)

    @property
    def sender_id(self):
        return self.sender.get('id')

    @property
    def recipient_id(self):
        return self.recipient.get('id')


class EchoEvent(Event):
    def __init__(self, message, **kwargs):
        super(EchoEvent, self).__init__(**kwargs)
        self.name = "echo"
        self.message = message

    @property
    def app_id(self):
        return self.message.get('app_id')

    @property
    def metadata(self):
        return self.message.get('metadata')

    @property
    def mid(self):
        return self.message.get('mid')

    @property
    def text(self):
        return self.message.get('text')


class MessageEvent(Event):
    def __init__(self, message, **kwargs):
        super(MessageEvent, self).__init__(**kwargs)
        self.name = "message"
        self.message = message

    @property
    def mid(self):
        return self.message.get('mid')

    @property
    def text(self):
        return self.message.get('text')

    @property
    def quick_reply(self):
        return self.message.get('quick_reply')

    @property
    def attachments(self):
        return self.message.get('attachments')


class PostbackEvent(Event):
    def __init__(self, postback, referral=None, **kwargs):
        super(PostbackEvent, self).__init__(**kwargs)
        self.name = "postback"
        self.postback = postback
        self.referral = referral if referral else {}

    @property
    def payload(self):
        return self.postback.get("payload")


class DeliveryEvent(Event):
    def __init__(self, delivery, **kwargs):
        super(DeliveryEvent, self).__init__(**kwargs)
        self.name = "delivery"
        self.delivery = delivery

    @property
    def mids(self):
        return self.delivery.get("mids")

    @property
    def watermark(self):
        return self.delivery.get("watermark")


class ReadEvent(Event):
    def __init__(self, read, **kwargs):
        super(ReadEvent, self).__init__(**kwargs)
        self.name = "read"
        self.read = read

    @property
    def watermark(self):
        return self.read.get("watermark")


class PassThreadControlEvent(Event):
    def __init__(self, pass_thread_control, **kwargs):
        super(PassThreadControlEvent, self).__init__(**kwargs)
        self.name = "pass_thread_control"
        self.pass_thread_control = pass_thread_control

    @property
    def new_owner_app_id(self):
        return self.pass_thread_control.get("new_owner_app_id")

    @property
    def metadata(self):
        return self.pass_thread_control.get("metadata")


class TakeThreadControlEvent(Event):
    def __init__(self, take_thread_control, **kwargs):
        super(TakeThreadControlEvent, self).__init__(**kwargs)
        self.name = "take_thread_control"
        self.take_thread_control = take_thread_control

    @property
    def previous_owner_app_id(self):
        return self.take_thread_control.get("previous_owner_app_id")

    @property
    def metadata(self):
        return self.take_thread_control.get("metadata")


class RequestThreadControlEvent(Event):
    def __init__(self, request_thread_control, **kwargs):
        super(RequestThreadControlEvent, self).__init__(**kwargs)
        self.name = "request_thread_control"
        self.request_thread_control = request_thread_control

    @property
    def previous_owner_app_id(self):
        return self.request_thread_control.get("requested_owner_app_id")

    @property
    def metadata(self):
        return self.request_thread_control.get("metadata")


class AccountLinkingEvent(Event):
    def __init__(self, account_linking, **kwargs):
        super(AccountLinkingEvent, self).__init__(**kwargs)
        self.name = "account_linking"
        self.account_linking = account_linking

    @property
    def status(self):
        return self.account_linking.get("status")

    @property
    def authorization_code(self):
        return self.account_linking.get("authorization_code")


class ReferralEvent(Event):
    def __init__(self, referral, **kwargs):
        super(ReferralEvent, self).__init__(**kwargs)
        self.name = "referral"
        self.referral = referral

    @property
    def source(self):
        return self.referral.get("source")

    @property
    def type(self):
        return self.referral.get("type")

    @property
    def ref(self):
        return self.referral.get("ref")

    @property
    def referer_uri(self):
        return self.referral.get("referer_uri")


class GameplayEvent(Event):
    def __init__(self, game_play, **kwargs):
        super(GameplayEvent, self).__init__(**kwargs)
        self.name = "game_play"
        self.game_play = game_play

    @property
    def game_id(self):
        return self.game_play.get("game_id")

    @property
    def player_id(self):
        return self.game_play.get("player_id")

    @property
    def context_id(self):
        return self.game_play.get("context_id")

    @property
    def score(self):
        return self.game_play.get("score")

    @property
    def payload(self):
        return self.game_play.get("payload")


class AppRolesEvent(Event):
    def __init__(self, app_roles, **kwargs):
        super(AppRolesEvent, self).__init__(**kwargs)
        self.name = "app_roles"
        self.app_roles = app_roles

    @property
    def ids(self):
        return list(self.app_roles.keys())


class PolicyEnforcementEvent(Event):
    def __init__(self, policy_enforcement, **kwargs):
        super(PolicyEnforcementEvent, self).__init__(**kwargs)
        self.name = "policy_enforcement"
        self.policy_enforcement = policy_enforcement

    @property
    def action(self):
        return self.policy_enforcement.get('reason')

    @property
    def reason(self):
        return self.policy_enforcement.get("reason")


class CheckoutUpdateEvent(Event):
    def __init__(self, **kwargs):
        super(CheckoutUpdateEvent, self).__init__(**kwargs)
        self.name = "checkout_update"
        """BETA NO DOCS"""


class PaymentEvent(Event):
    def __init__(self, **kwargs):
        super(PaymentEvent, self).__init__(**kwargs)
        self.name = "payment"
        """BETA NO DOCS"""


class OptinEvent(Event):
    def __init__(self, optin, **kwargs):
        super(OptinEvent, self).__init__(**kwargs)
        self.name = "optin"
        self.optin = optin

    @property
    def ref(self):
        return self.optin.get("ref")

    @property
    def user_ref(self):
        return self.optin.get("user_ref")


class StandByEvent(Event):
    def __init__(self, standby, **kwargs):
        super(StandByEvent, self).__init__(**kwargs)
        self.name = "standby"
        self.standby = standby



