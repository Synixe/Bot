import urllib.request
import json
import discord

GITHUB = {
    "acemod" : ["ACE3"],
    "CBATeam" : ["CBA_A3"]
}

class Commands():
    def register(self, client):
        self.mod_loop = client.loop.create_task(self.mod_loop_task(client))
        return {}

    async def mod_loop_task(self, client):
        await client.wait_until_ready()
        while not client.is_closed():
            print("Mod Loop Started")
            with open("./data/mods.json") as f:
                current = json.loads(f.read().decode("UTF-8"))
            for author in GITHUB:
                for repo in GITHUB[author]:
                    version = latest(author,repo)
                    print(version)
                    if version != current[author+"/"+repo]:
                        print("Update to:",repo,version)
            await asyncio.sleep(60 * 30) #Check every 30 minutes

def latest(owner, repo):
    f = urllib.request.urlopen("https://api.github.com/repos/"+owner+"/"+repo+"/releases")
    data = json.loads(f.read().decode("UTF-8"))
    return data[0]["tag_name"]
