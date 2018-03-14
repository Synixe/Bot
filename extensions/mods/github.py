import urllib.request
import json

"""GitHub Helper Functions"""
def latest(repo):
    """Get the latest release version"""
    req = urllib.request.urlopen("https://api.github.com/repos/"+repo+"/releases")
    data = json.loads(req.read().decode("UTF-8"))
    return data[0]["tag_name"]
