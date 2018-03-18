import urllib.request
import json

"""GitHub Helper Functions"""
def latest(repo):
    """Get the latest release version"""
    req = urllib.request.Request("https://api.github.com/repos/"+repo+"/releases")
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("UTF-8"))
    return data[0]["tag_name"]
