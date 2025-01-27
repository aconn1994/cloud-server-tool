from html.parser import HTMLParser

class MyHTMLParser(HTMLParser): # TO BE CONTINUED.............
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag: ", tag)

    def handle_data(self, data):
        print("Encountered some data: ", data)

def parse_mod_file(mod_file) -> None:
    html_parser = MyHTMLParser()
    mf = open(mod_file, "r")
    html_parser.feed(mf.read())
