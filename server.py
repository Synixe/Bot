import discord
import re
import asyncio
import os

SERVERS = {"arma3":"Primary Arma 3"}

REGEX_PROGRESS = r"progress: (\d.?\.\d\d)"
REGEX_LOGIN = r"Logged in OK"

class Commands():
    def register(self, _):
        return {
            "start" : {
                "function" : self.start,
                "description" : "Start ",
                "roles" : ["manager","moderator"]
            },
            "steam" : {
                "function" : self.steam,
                "description" : "Download a steam server",
                "roles" : ["manager"]
            }
        }

    async def start(self, data, client, message):
        if data[0].lower() not in SERVERS:
            await message.channel.send("Unknown Server")
        else:
            if data[0].lower() == "arma3":
                import subprocess
                r = subprocess.run(["systemctl","is-active","arma3-mod"], stdout=subprocess.PIPE)
                if r.stdout.decode("UTF-8")[:-1] == "active":
                    await message.channel.send("The Arma 3 Server is already running.")
                else:
                    os.system("sudo systemctl start arma3-mod")
                    await message.channel.send("Starting Arma 3 Server")
            else:
                await message.channel.send("Unable to start: "+SERVERS[data[0].lower()])

    async def steam(self, data, client, message):
        if len(data) != 2:
            await message.channel.send("Invalid arguments")
            return
        if ".." in data[1] or "~" in data[1] or data[1].startswith("/"):
            print("Invalid Directory")
            return

        await message.channel.send("App ID: "+data[0]+"\nDirectory: /opt/steam/"+data[1]+"/\nIs this correct? (y/n)")
        def question_check(m):
            return m.author == message.author
        def getRegex(regex, string):
            matches = re.search(regex, string)
            if matches:
                try:
                    return matches.group(1)
                except:
                    return True
            return False
        try:
            confirm = await client.wait_for('message', check=question_check, timeout=60.0)
            if confirm.content.lower() != "y":
                await message.channel.send("This operation has been cancelled.")
                return
            import subprocess
            import sys
            import os
            import time
            import re
            process = subprocess.Popen(
                [
                    "/opt/steam/steamcmd.sh",
                    "+login",
                    "anonymous",
                    "+force_install_dir",
                    "/opt/steam/"+data[1]+"/",
                    "+app_update",
                    data[0],
                    "validate",
                    "+quit"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            logged = False
            text = "SteamCMD Logged In & Ready\nProgress: 0.00%\n"
            while True:
                out = process.stdout.readline().decode("UTF-8")
                if out == '' and process.poll() != None:
                    break
                if out != '':
                    if not logged:
                        if getRegex(REGEX_LOGIN, out):
                            logged = True
                            id = await message.channel.send(text)
                    if logged:
                        progress = getRegex(REGEX_PROGRESS, out)
                        if progress == False:
                            progress = "0.00"
                        text = "\n".join(text.split("\n")[:-1])+"\nProgress: "+progress+"%"
                        await id.edit(content=text)
                    if "Success" in out:
                        text = "\n".join(text.split("\n")[:-1])+"\nProgress: 100.00%"
                        text += "\nDownloaded"
                        await id.edit(content=text)
                        break

        except asyncio.TimeoutError:
            await id.channel.send("Timeout, this operation has been cancelled.")
            return
