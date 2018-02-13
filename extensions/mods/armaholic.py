"""Armaholic Helper Functions"""
import urllib.request
import re

def latest(mod):
    """Get the latest version of a mod"""
    req = urllib.request.urlopen("http://armaholic.com/page.php?id="+str(mod))
    html = req.read().decode("UTF-8")
    return re.search(r"Version\:<\/font> (.+?)<br>", html).group(1).strip()
