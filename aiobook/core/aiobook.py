from aiohttp import web

from aiobook.core.facebook.handler import FacebookHandler


class AioBookApp:
    def __init__(self, port):
        self.app = web.Application()
        self.port = port

    def register_messenger(self, messenger: FacebookHandler):
        self.app.add_routes([web.get(messenger.urlpath, messenger.handle_get),
                             web.post(messenger.urlpath, messenger.handle_post)])

    def register_handler(self, type_request, urlpath, func):
        if type_request == 'get':
            self.app.add_routes([web.get(urlpath, func)])
        elif type_request == 'post':
            self.app.add_routes([web.post(urlpath, func)])

    def start_bot(self):
        web.run_app(self.app, port=self.port)
