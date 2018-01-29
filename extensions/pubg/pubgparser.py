from html.parser import HTMLParser
import json

class PUBGParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.check_next = True

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.check_next:
            self.check_next = False
            if data.startswith("var playerData = "):
                self.data = json.loads(data[17:-1])

    def process(self):
        self.data['lifetime'] = {}
        self.data['solo'] = {}
        self.data['duo'] = {}
        self.data['squad'] = {}
        self.data['solo-fpp'] = {}
        self.data['duo-fpp'] = {}
        self.data['squad-fpp'] = {}
        for k in self.data['LifeTimeStats']:
            self.data['lifetime'][k['Key'].replace("Matches Played","Rounds Played")] = k['Value']

        for m in self.data["Stats"]:
            mode = self.data[m['Match']]
            for s in m['Stats']:
                mode[s['label']] = s['value']
