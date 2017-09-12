import json

def getToken(service):
    with open("tokens.json") as f:
        data = json.loads(f.read())
    if service in data:
        return data[service]
    else:
        return None
