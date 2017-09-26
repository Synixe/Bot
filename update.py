import urllib.request
import json
import discord
import asyncio
import re

GITHUB = {
    "acemod": ["ACE3"],
    "CBATeam": ["CBA_A3"],
    "Synixe": ["TFAR-ACE"],
    "DerZade": ["BackpackOnChest"]
}

ARMAHOLIC = {
    "30461": "3den Enhanced",
    "30367": "Advanced Sling Loading",
    "30575": "Advanced Towing",
    "23899": "Blastcore: Phoenix 2",
    "32595": "Zeus FPS Monitor",
    "27224": "Enhanced Movement",
    "26780": "Enhanced Soundscape",
    "27996": "Gorgona",
    "29327": "ShackTac User Interface",
    "25381": "Vcom AI",
    "27285": "Ares",
    "31357": "Advanced Urban Rappelling",
    "22594": "F/A-18 Super Hornet"
}

REGEX = r"Version\:<\/font> (.+?)<br>"

MOD_FILE = "./data/mods.json"

class Commands():
    def register(self, client):
        self.mod_loop = client.loop.create_task(self.mod_loop_task(client))
        return {}

    async def mod_loop_task(self, client):
        await client.wait_until_ready()
        while not client.is_closed():
            print("Mod Loop Started")
            with open(MOD_FILE) as f:
                current = json.loads(f.read())
            update = False
            for author in GITHUB:
                for repo in GITHUB[author]:
                    version = latest(author,repo)
                    if version.strip() != current[author+"/"+repo].strip():
                        update = True
                        current[author+"/"+repo] = version.strip()
                        await client.getChannel(client.getGuild("Synixe"),"botevents").send("Update to: "+repo+" "+version)
            for mod in ARMAHOLIC:
                f = urllib.request.urlopen("http://armaholic.com/page.php?id="+str(mod))
                html = f.read().decode("UTF-8")
                version = re.search(REGEX, html).group(1)
                if version.strip() != current[ARMAHOLIC[mod]].strip():
                    update = True
                    current[ARMAHOLIC[mod]] = version.strip()
                    await client.getChannel(client.getGuild("Synixe"),"botevents").send("Update to: "+ARMAHOLIC[mod]+" "+version+"\nhttp://armaholic.com/page.php?id="+str(mod))
            if update:
                with open(MOD_FILE,"w") as f:
                    f.write(json.dumps(current, indent=4, sort_keys=True))
            await asyncio.sleep(60 * 60)

def latest(owner, repo):
    f = urllib.request.urlopen("https://api.github.com/repos/"+owner+"/"+repo+"/releases")
    data = json.loads(f.read().decode("UTF-8"))
    return data[0]["tag_name"]
