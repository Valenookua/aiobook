import json


class Button(object):
    def __init__(self, type):
        self.type = type

    def to_json(self):
        return json.dumps(self, default=lambda i: i.__dict__)


class CallButton(Button):
    def __init__(self, title, payload):
        super(CallButton, self).__init__("phone_number")
        self.payload = payload
        self.title = title


class GamePlayButton(Button):
    def __init__(self, title, payload, player_id=None, contex_id=None):
        super(GamePlayButton, self).__init__("game_play")
        self.payload = json.dumps(payload)
        self.title = title
        if player_id and contex_id:
            raise ValueError("Only one of the player_id or contex_id must be specified")
        elif not player_id and not contex_id:
            pass
        else:
            self.game_metadata = {"player_id": player_id}\
                if player_id else {"contex_id": contex_id}


class LogInButton(Button):
    def __init__(self, url):
        super(LogInButton, self).__init__("account_link")
        self.url = url


class LogOutButton(Button):
    def __init__(self):
        super(LogOutButton, self).__init__("account_unlink")


class PostbackButton(Button):
    def __init__(self, title, payload):
        super(PostbackButton, self).__init__("postback")
        self.title = title
        self.payload = payload


class UrlButton(Button):
    def __init__(self, url, title=None,
                 webview_height_ratio=None,
                 messenger_extensions=None,
                 fallback_url=None,
                 webview_share_button=None):
        super(UrlButton, self).__init__("web_url")
        self.url = url
        if title:
            self.title = title
        if webview_height_ratio != "compact" \
                or webview_height_ratio != "tall"\
                or webview_height_ratio != "full"\
                or not webview_height_ratio:
            self.webview_height_ratio = webview_height_ratio
        else:
            raise ValueError("webview_height_ratio must be \"compact\", \"tall\" or \"full\"")
        if messenger_extensions is True:
            self.messenger_extensions = messenger_extensions
            if fallback_url:
                self.fallback_url = fallback_url
        self.webview_share_button = webview_share_button
