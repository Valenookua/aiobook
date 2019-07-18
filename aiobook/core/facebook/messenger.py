import asyncio
import warnings

import aiohttp

from .handler import FacebookHandler

from .types.send_api import Response, Recipient, Message, Attachment, PersistentMenu


class MessengerWarning(UserWarning):
    """"""


class Messenger(object):
    def __init__(self, page_access_token, verify_token, urlpath="", **kwargs):
        self.handler = FacebookHandler(page_access_token, verify_token, **kwargs)
        self.page_access_token = page_access_token
        self.urlpath = urlpath
        self.api_ver = kwargs.pop('api_ver', 'v3.3')

    def get_url(self, suffix):
        return f"https://graph.facebook.com/{self.api_ver}/{suffix}"

    @staticmethod
    async def _api_call_post(url, data):
        async with aiohttp.ClientSession() as session:
            print(data)
            headers = {'Content-type': 'application/json'}
            async with session.post(url=url,
                                    data=data,
                                    headers=headers) as response:
                response = await response.json()
                print('r_post', response)
                if response.get('error'):
                    warnings.warn(f"POST request returns error: {response['error']}",
                                  MessengerWarning)
            return response

    @staticmethod
    async def _api_call_get(url, params):
        async with aiohttp.ClientSession() as session:
            headers = {'Content-type': 'application/json'}
            async with session.get(url=url,
                                   params=params,
                                   headers=headers) as response:
                response = await response.json()
                if response.get('error'):
                    warnings.warn(f"GET request returns error: {response['error']}",
                                  MessengerWarning)
            return response

    async def get_user_profile(self, psid, fields=("first_name", "last_name")):
        params = {"fields": f"{','.join(fields)}", "access_token": self.page_access_token}
        response = await self._api_call_get(self.get_url(f"{psid}"), params)
        return response

    async def get_page_info(self):
        params = {"access_token": self.page_access_token}
        response = await self._api_call_get(self.get_url(f"me"), params)
        return response

    async def send(self, recipient_id, message, quick_replies=None,
                   messaging_type=None, metadata=None, notification_type=None,
                   tag=None):
        text = message if isinstance(message, str) else None
        attachment = Attachment("template", message) if not text else None
        data = Response(recipient=Recipient(id_=recipient_id),
                        message=Message(text=text,
                                        attachment=attachment,
                                        quick_replies=quick_replies,
                                        metadata=metadata),
                        messaging_type=messaging_type,
                        notification_type=notification_type,
                        tag=tag).to_json()
        await self._api_call_post(self.get_url(f"me/messages?access_token"
                                               f"={self.page_access_token}"), data)


    async def set_persistent_menu(self, persistent_menu):
        raise NotImplementedError
        #data = PersistentMenu(persistent_menu=persistent_menu).to_json()
        #await self._api_call_post(self.get_url(f"me/messages?access_token"
        #                                       f"={self.page_access_token}"), data)

    async def typing_on(self, recipient_id):
        data = Response(recipient=Recipient(id_=recipient_id),
                        messaging_type=None,
                        message=None,
                        sender_action="typing_on").to_json()
        await self._api_call_post(self.get_url(f"me/messages?access_token"
                                               f"={self.page_access_token}"), data)

    async def typing_off(self, recipient_id):
        data = Response(recipient=Recipient(id_=recipient_id),
                        messaging_type=None,
                        message=None,
                        sender_action="typing_off").to_json()
        await self._api_call_post(self.get_url(f"me/messages?access_token"
                                               f"={self.page_access_token}"), data)

    async def mark_seen(self, recipient_id):
        data = Response(recipient=Recipient(id_=recipient_id),
                        messaging_type=None,
                        message=None,
                        sender_action="mark_seen").to_json()
        await self._api_call_post(self.get_url(f"me/messages?access_token"
                                               f"={self.page_access_token}"), data)

    def imitate_typing(self, time_to_sleep=0):
        def decorator(func):
            async def wrapper(event, *args, **kwargs):
                await self.mark_seen(event.sender_id)
                await self.typing_on(event.sender_id)
                await asyncio.sleep(time_to_sleep)
                await func(event, *args, **kwargs)
                await self.typing_off(event.sender_id)
            return wrapper
        return decorator
