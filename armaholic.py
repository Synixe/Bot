import requests
import re

URL_REGEX = r"<form method=\"post\" action=\"(.+?)\">"
CAP_REGEX = r"name=\"submit\" value=\"(.+?)\""
RAN_REGEX = r"name=\"x\" value=\"(.+?)\""

data={"x":"3910CD8F","captcha":"I am a human!","super":"","submit":"Click to download Advanced Urban Rappelling"}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',"Referer":"http://www.armaholic.com/page.php?id=31357"}
id = input("Mod ID: ")
html = requests.get("http://www.armaholic.com/page.php?id="+id,headers=headers).text
url = re.search(URL_REGEX, html).group(1)
cap = re.search(CAP_REGEX, html).group(1)
ran = re.search(RAN_REGEX, html).group(1)
data['submit'] = cap
data['x'] = ran

req = requests.post(url, data, headers=headers)
with open(id+"."+url.split(".")[-1],"wb") as file:
    file.write(req.content)
