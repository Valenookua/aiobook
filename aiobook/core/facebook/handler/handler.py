import asyncio
import warnings

from aiohttp import web

from aiobook.core.facebook.handler.events import *


class WebhookHandlerWarning(UserWarning):
    """"""


class FacebookHandler(object):
    def __init__(self, page_access_token, verify_token, **kwargs):
        """
        :param page_access_token:
        :param verify_token:
        :param kwargs:
        """
        self.page_access_token = page_access_token
        self.verify_token = verify_token
        self.skip_confirm_execution = kwargs.pop('skip_confirm_execution', False)

    _webhook_handlers = {}
    _webhook_endpoints = ("before_handle", "after_handle", "echo", "message", "postback",
                          "delivery", "read", "pass_thread_control", "take_thread_control",
                          "request_thread_control",
                          "account_linking", "referral", "game_play", "app_roles",
                          "policy_enforcement",
                          "checkout_update", "payment", "optin", "stand_by")

    async def handle_get(self, request):
        """
        :param request:
        :return:
        """
        args = request.rel_url.query
        if args.get('hub.mode') == 'subscribe' and args.get('hub.challenge'):
            if not args.get('hub.verify_token') == self.verify_token:
                return web.Response(text='Verification token mismatch', status=403)
            return web.Response(body=args['hub.challenge'], status=200)
        return web.Response(text='OK', status=200)

    async def handle_post(self, request):
        """
        :param request:
        :return:
        """
        raw_request = await request.json()
        if raw_request.get("object") != "page":
            response = web.Response(text="Unsupported request", status=403)
        else:
            if raw_request['entry']:
                for entry in raw_request['entry']:
                    if self.skip_confirm_execution:
                        asyncio.create_task(self._handle_webhook(entry))
                        response = web.Response(text="OK", status=200)
                    else:
                        response = await self._handle_webhook(entry)
            else:
                warnings.warn(f"Can't handle request: missed field \"entry\"",
                              WebhookHandlerWarning)
                response = web.Response(text="Unsupported request", status=403)

        return response

    @staticmethod
    def _event_create(message):
        if "message" in message.keys():
            if message["message"].get("is_echo"):
                event = EchoEvent.from_json(message)
            else:
                event = MessageEvent.from_json(message)
        elif "postback" in message.keys():
            event = PostbackEvent.from_json(message)
        elif "delivery" in message.keys():
            event = DeliveryEvent.from_json(message)
        elif "read" in message.keys():
            event = ReadEvent.from_json(message)
        elif "pass_thread_control" in message.keys():
            event = PassThreadControlEvent.from_json(message)
        elif "take_thread_control" in message.keys():
            event = TakeThreadControlEvent.from_json(message)
        elif "request_thread_control" in message.keys():
            event = RequestThreadControlEvent.from_json(message)
        elif "account_linking" in message.keys():
            event = AccountLinkingEvent.from_json(message)
        elif "referral" in message.keys():
            event = ReferralEvent.from_json(message)
        elif "game_play" in message.keys():
            event = GameplayEvent.from_json(message)
        elif "app_roles" in message.keys():
            event = AppRolesEvent.from_json(message)
        elif "policy_enforcement" in message.keys():
            event = PolicyEnforcementEvent.from_json(message)
        elif "checkout_update" in message.keys():
            event = CheckoutUpdateEvent.from_json(message)
        elif "payment" in message.keys():
            event = PaymentEvent.from_json(message)
        elif "optin" in message.keys():
            event = OptinEvent.from_json(message)
        elif "standby" in message.keys():
            event = StandByEvent.from_json(message)
        else:
            warnings.warn(f"Got unknown event", WebhookHandlerWarning)
            event = Event.from_json(message)
        return event

    async def _handle_webhook(self, body):
        if "messaging" in body.keys():
            for message in body['messaging']:
                event = self._event_create(message)

                if self._webhook_handlers.get('before_handle'):
                    await self._call_handler(event.name, event)

                await self._call_handler(event.name, event)

                if self._webhook_handlers.get('after_handle'):
                    await self._call_handler(event.name, event)

        elif "standby" in body.keys():
            for message in body['standby']:
                event = self._event_create(message)
                await self._call_handler(event.name, event)

        response = web.Response(text="OK", status=200)
        return response

    async def _call_handler(self, name, *args, **kwargs):
        if name in self._webhook_handlers:
            await self._webhook_handlers[name](*args, **kwargs)
        else:
            warnings.warn(f"There are not \"{name}\" handler defined! Call skipped",
                          WebhookHandlerWarning)

    def get_defined_handlers(self):
        return list(self._webhook_handlers.keys())

    def set_webhook_handler(self, name, func):
        if name not in self._webhook_endpoints:
            warnings.warn(f"The handler \"{name}\" call will never happen.",
                          WebhookHandlerWarning)
        self._webhook_handlers[name] = func

    def before_handle(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["before_handle"] = func

    def after_handle(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["after_handle"] = func

    def handle_echo(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["echo"] = func

    def handle_message(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["message"] = func

    def handle_postback(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["postback"] = func

    def handle_delivery(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["delivery"] = func

    def handle_read(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["read"] = func

    def handle_pass_thread_control(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["pass_thread_control"] = func

    def handle_take_thread_control(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["take_thread_control"] = func

    def handle_request_thread_control(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["request_thread_control"] = func

    def handle_account_linking(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["account_linking"] = func

    def handle_referral(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["referral"] = func

    def handle_game_play(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["game_play"] = func

    def handle_app_roles(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["app_roles"] = func

    def handle_policy_enforcement(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["policy_enforcement"] = func

    def handle_checkout_update(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["checkout_update"] = func

    def handle_payment(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["payment"] = func

    def handle_optin(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["optin"] = func

    def handle_standby(self, func):
        """
        :param func:
        :return:
        """
        self._webhook_handlers["stand_by"] = func
