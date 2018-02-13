"""Reads HTML to extract Rainbow 6 Siege Data"""
from html.parser import HTMLParser

class R6Parser(HTMLParser):
    """Rainbow 6 Siege HTML Parser"""
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            attrs = dict(attrs)
            if "data-stat" in attrs:
                if attrs["data-stat"] == "PVPDeaths":
                    self.deaths = "NEXT"
                elif attrs["data-stat"] == "PVPKills":
                    self.kills = "NEXT"
                elif attrs["data-stat"] == "PVPWLRatio":
                    self.wlr = "NEXT"
                elif attrs["data-stat"] == "PVPAccuracy":
                    self.accuracy = "NEXT"
        elif tag == "img":
            attrs = dict(attrs)
            if "class" in attrs:
                if attrs['class'] == "profile-avatar":
                    self.profile = attrs['src']
        elif tag == "h1":
            attrs = dict(attrs)
            if "class" in attrs:
                if attrs['class'] == "profile-name":
                    self.name = "NEXT"

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.deaths == "NEXT":
            self.deaths = data
        elif self.kills == "NEXT":
            self.kills = data
        elif self.wlr == "NEXT":
            self.wlr = data
        elif self.accuracy == "NEXT":
            self.accuracy = data
        elif self.name == "NEXT":
            self.name = data
