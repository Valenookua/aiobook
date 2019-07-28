# AioBook

AioBook it is async framework for build messenger application in facebook

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install aiobook.

```bash
pip install aiobook
```

# Usage
## Facebook Handler

Facebook Handler can handle all [facebook webhook events](https://developers.facebook.com/docs/messenger-platform/webhook)

You can use decorators:
```python
from aiobook import FacebookHandler
handler = FacebookHandler("<page_access_token", "<verification_token>", skip_confirm_execution=True)

@handler.handle_message
async def handle_message(event):
    print("receive your message {}".format(event.text))
    
@handler.handle_postback
async def handle_postback(event):
    print("receive your postback with payload {}".format(event.postback))
```
Or directly register handlers:
```python
async def handle_message(event):
    print("receive your message {}".format(event.text))
    
async def handle_postback(event):
    print("receive your postback with payload {}".format(event.postback))

handler.set_webhook_handler("message", handle_message)
handler.set_webhook_handler("postback", handle_postback)
```
To get list allowed and defined handlers:
```python
handler.get_allowed_handlers()
handler.get_defined_handlers()
```
Also you can set handler before_handle, and after_handle. It will be called before(or after) handle_event:
```python
@handler.before_handle
async def log_message(event):
    logging.info("{} handled.".format(event.name))

@handler.after_handle
async def log_message(event):
    logging.info("{} handled.".format(event.name))

```

To receive message you need register handler in HTTP Server:
```python
from aiohttp import web
from aiobook import FacebookHandler
handler = FacebookHandler("<page_access_token", "<verification_token>", skip_confirm_execution=True)
app = web.Application()
app.add_routes([web.get("<url_pattern>", handler.handle_get)])
app.add_routes([web.post("<url_pattern>", handler.handle_post)])
```

## Messenger
Messenger supports [Send API method](https://developers.facebook.com/docs/messenger-platform/reference/send-api).
 Facebook Handler included in Messenger.
```python
from aiobook import Messenger
messenger = Messenger("<page_access_token", "<verification_token>", skip_confirm_execution=True)

@messenger.handler.handle_message
async def handle_message(event):
    await messenger.send(event.sender_id, "Your message: {}".format(event.text))
    
@messenger.handler.handle_postback
async def handle_postback(event):
    await messenger.send(event.sender_id, "Your press button: {}".format(event.postback))
```
### messenger.send
Allow to send text or templates:
```python
await messenger.send(event.sender_id, message, quick_replies=None,
                   messaging_type=None, metadata=None, notification_type=None,
                   tag=None)
```
#### Allowed types for messenger.send
String message and templates
##### Supported Templates
ButtonTemplate, GenericTemplate, ListTemplate, OpenGraphTemplate, MediaTemplate.
##### Supported Buttons
CallButton, GamePlayButton, LogInButton, LogOutButton, PostbackButton, UrlButton
##### Other
QuickReply, Element, MediaElement, OpenGraphElement
```python
from aiobook.core.facebook import QuickReply
from aiobook.core.facebook import Element, MediaElement, OpenGraphElement
from aiobook.core.facebook import ButtonTemplate, GenericTemplate, ListTemplate, OpenGraphTemplate, MediaTemplate
from aiobook.core.facebook import CallButton, GamePlayButton, LogInButton, LogOutButton, PostbackButton, UrlButton

await messenger.send(event.sender_id,
 ButtonTemplate('Hi, press buttons',
  buttons=[PostbackButton('test', 'test_payload'),
           UrlButton(title='test_rl', url='https://www.messenger.com')]))

await messenger.send(event.sender_id,
 GenericTemplate([Element('test',
                         buttons=[PostbackButton('test', 'test_payload'),
                                  UrlButton(title='test_rl', url='https://www.messenger.com')]),
                 Element('test2', image_url, 'test2',
                         buttons=[PostbackButton('test', 'test_payload'),
                                  UrlButton(title='test_rl', url='https://www.messenger.com')])]))

```
### messenger.get_user_profile
Allows you to use a sender_id to retrieve user profile information:
```python
response = await messenger.get_user_profile(event.sender_id, fields=("first_name", "last_name"))
```
Next fields are [supported](https://developers.facebook.com/docs/messenger-platform/identity/user-profile).

### messenger.get_page_info
Allows you to retrieve your page information:
```python
response = await messenger.get_page_info()
```


### messenger.imitate_typing
Decorate func to imitate typing with defined timeout before answer. Included mark_seen, typing_on
and typing_off sender_actions.
```python
@messenger.handler.handle_postback
@messenger.imitate_typing(1)  
async def handle_postback(event):
    await messenger.send(event.sender_id, "Your press button: {}".format(event.postback))
```
Or you can use sender actions independently:
#### messenger.mark_seen
Sender action to mark last message as read
```python
await messenger.mark_seen(event.sender_id)
```
#### messenger.typing_on
Sender action to turn typing indicators on
```python
await messenger.typing_on(event.sender_id)
```
#### messenger.typing_off
Sender action to turn typing indicators off
```python
await messenger.typing_off(event.sender_id)
```


## AioBook App
AioBook it is small aiohttp wrapper that helps manage and deploy your messenger app
```python
from aiobook import AioBookApp
from aiobook import Messenger
app = AioBookApp(port=3000)
messenger = Messenger("<page_access_token", "<verification_token>", skip_confirm_execution=True)
app.register_messenger(messenger)
app.start_bot()
```

## License
[MIT](https://choosealicense.com/licenses/mit/)