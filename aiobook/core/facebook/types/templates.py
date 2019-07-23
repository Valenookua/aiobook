import json


class Template(object):
    def __init__(self, template_type):
        self.template_type = template_type

    def to_json(self):
        return json.dumps(self, default=lambda i: i.__dict__)


class ButtonTemplate(Template):
    def __init__(self, text, buttons):
        super(ButtonTemplate, self).__init__("button")
        self.text = text
        if not isinstance(buttons, list):
            raise ValueError(f"buttons must be a list, got {type(buttons)}")
        self.buttons = buttons

        if len(self.buttons) > 3:
            raise ValueError("Button Template support up to 3 buttons only")


class GenericTemplate(Template):
    def __init__(self, elements):
        super(GenericTemplate, self).__init__("generic")

        if not isinstance(elements, list):
            raise ValueError(f"elements must be a list, got {type(elements)}")
        self.elements = elements
        if len(self.elements) > 10:
            raise ValueError("Button Template support up to 10 buttons only")


class ListTemplate(Template):
    def __init__(self, top_element_style, elements, buttons):
        super(ListTemplate, self).__init__("list")
        self.top_element_style = top_element_style
        if self.top_element_style != "compact" or self.top_element_style != 'large':
            raise ValueError("top_element_style must be \"compact\" or \"large\"")

        if not isinstance(elements, list):
            raise ValueError(f"elements must be a list, got {type(elements)}")
        self.elements = elements

        if len(self.elements) > 4 and len(self.elements) < 2:
            raise ValueError("List Template support 2-4 elements only")

        if buttons:
            if not isinstance(buttons, list):
                raise ValueError(f"buttons must be a list, got {type(buttons)}")
            self.buttons = buttons
            if len(self.buttons) > 1:
                raise ValueError("List Template support only 1 button")


class OpenGraphTemplate(Template):
    def __init__(self, elements):
        super(OpenGraphTemplate, self).__init__("open_graph")
        if not isinstance(elements, list):
            raise ValueError(f"elements must be a list, got {type(elements)}")
        self.elements = elements
        if len(self.elements) > 1:
            raise ValueError("Open Graph Template support 1 element only")


class MediaTemplate(Template):
    def __init__(self, elements):
        super(MediaTemplate, self).__init__("media")
        if not isinstance(elements, list):
            raise ValueError(f"elements must be a list, got {type(elements)}")
        self.elements = elements
        if len(self.elements) > 1:
            raise ValueError("Media Template support 1 element only")


class ReceiptTemplate(Template):
    def __init__(self):
        raise NotImplementedError


class AirlineTemplate(Template):
    def __init__(self):
        raise NotImplementedError
