import parser
import urllib.request

req = urllib.request.Request(url="https://raw.githubusercontent.com/Synixe/Documents/master/SynixeConstitution.tex",headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
with urllib.request.urlopen(req) as response:
    tex = parser.Parser(response.read().decode("UTF-8"))

print(tex.getByID("6.4.3"))
