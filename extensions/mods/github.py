def latest(owner, repo):
    f = urllib.request.urlopen("https://api.github.com/repos/"+repo+"/releases")
    data = json.loads(f.read().decode("UTF-8"))
    return data[0]["tag_name"]
