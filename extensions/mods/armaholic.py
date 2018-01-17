import urllib.request
import re

def latest(mod):
    f = urllib.request.urlopen("http://armaholic.com/page.php?id="+str(mod))
    html = f.read().decode("UTF-8")
    return re.search(r"Version\:<\/font> (.+?)<br>", html).group(1).strip()
