from html.parser import HTMLParser
from typing import Any


class ArmaThreeHTMLParser(HTMLParser):  # TO BE CONTINUED.............
    def __init__(self, utils: Any):
        super(ArmaThreeHTMLParser, self).__init__()
        self.utils = utils
        self.html_as_dict: dict[str, str | None] = {}
        self.start_tag: str | None = None
        self.is_display_name: bool | None = False
        self.display_name: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple]):
        if tag == "td":
            for attr in attrs:
                if attr[0] == "data-type" and attr[1] == "DisplayName":
                    self.start_tag = tag
                    self.is_display_name = True
        elif tag == "a":
            self.start_tag = tag

    def handle_data(self, data: str):
        if self.start_tag == "td" and self.is_display_name:
            self.display_name = self.utils.reformat_string(data, "")
            self.html_as_dict[self.display_name] = None
            self.is_display_name = False
        elif self.start_tag == "a" and self.display_name:
            self.html_as_dict[self.display_name] = data.split("=")[1]
            self.display_name = None
