==================
Aiobook Changelog
==================

Version 0.1.2 (28 July 2019)
----------------------------
* Added:
    * **setup.py**: long description
* Changed:
    * **FacebookHandler.get_defined_handlers()**: it returns tuple now
* Fixed:
    * **FacebookHandler.get_allowed_handlers()**: doesn't work
    * **README.md**: several mistypings

Version 0.1.1 (25 July 2019)
----------------------------
* Fixed:
    * **Messenger.send()**: "allowed types" was unallowed
    * **setup.py**:  pip install didn't install package correctly
    * **README.md**: several mistypings


Version 0.1.0 (23 July 2019)
----------------------------
* **Initial release**
* Added:
    * Facebook event handler
    * Send API functionality
    * Types for send API (Templates, Buttons, Elements, Quick Replies)
    * AioBookApp wrapper