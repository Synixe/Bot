import discord
import requests
import json

import certs

class Commands():
    def register(self, _):

        return {
            "missionup" : {
                "function" : self.missionup,
                "description" : "Upload a mission to the server",
                "roles" : ["missionmaker"]
            },

            "slot" : {
                "function" : self.slot,
                "description" : "Slot into the current event",
                "roles" : ["@everyone"]
            },
            "unslot" : {
                "function" : self.unslot,
                "description" : "Unslot from the current event",
                "roles" : ["@everyone"]
            },
            "post" : {
                "function" : self.post,
                "description" : "Post an event to #events",
                "roles" : ["manager"]
            }
        }

    async def missionup(self, data, client, message):
        for attach in message.attachments:
            id = await message.channel.send("Downloading "+attach.filename)
            with open("/opt/steam/arma3-mods/mpmissions/"+attach.filename,'wb') as f:
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                f.write(requests.get(attach.url, headers=headers).content)
            await id.edit(content="Downloaded "+attach.filename)

    async def unslot(self, data, client, message):
        await self._unslot(message.channel.guild, message.author.id, message.channel)

    async def _unslot(self, guild, id, reply=None):
        channel = self.getEventChannel(guild)
        async for log in channel.history(limit=5):
            if log.content.startswith("|EVENT"):
                lines = log.content.split("\n")
                fname = lines[0].split(": ")[1][:-1]
                f = open("./missions/"+fname)
                post = json.loads(f.read())
                f.close()
                for s in post['slots']:
                    for r in s['slots']:
                        if "playerid" in r:
                            if str(r['playerid']) == str(id):
                                del r['playerid']
                                del r['player']
                                await self.savePost(fname, post)
                                if reply != None:
                                    await reply.send("Unslotted :cry:")
                                    await self.displayEvent(reply.guild, fname, log)
                                return
                if reply != None:
                    await reply.send("You were not slotted.")
                return

    async def slot(self, data, client, message):
        role = data[0]
        channel = self.getEventChannel(message.channel.guild)
        async for log in channel.history(limit=5):
            if log.content.startswith("|EVENT"):
                lines = log.content.split("\n")
                fname = lines[0].split(": ")[1][:-1]
                await self._unslot(message.channel.guild, message.author.id)
                f = open("./missions/"+fname)
                post = json.loads(f.read())
                f.close()
                for s in post['slots']:
                    for r in s['slots']:
                        if role.lower() in r['name'].lower():
                            if "playerid" not in r:
                                if "requirement" in r:
                                    qualified = certs.isQualified(message.author.id, r["requirement"])
                                    if qualified:
                                        r['player'] = message.author.name
                                        r['playerid'] = message.author.id
                                        await message.channel.send("Slotted "+message.author.name+" into "+r['name'])
                                        await self.savePost(fname,post)
                                        await self.displayEvent(message.channel.guild, fname, log)
                                        return
                                    else:
                                        await message.channel.send("You are missing the following certifications: "+(", ".join(qualified)))
                                        return
                                else:
                                    r['player'] = message.author.name
                                    r['playerid'] = message.author.id
                                    await message.channel.send("Slotted "+message.author.name+" into "+r['name'])
                                    await self.savePost(fname,post)
                                    await self.displayEvent(message.channel.guild, fname, log)
                                    return
                            else:
                                await message.channel.send(r['name'] + " is already slotted by "+r['player']+"!")
                                return
                await message.channel.send(role+" not found for "+post['name'])
                return

    async def post(self, data, client, message):
        channel = self.getEventChannel(message.channel.guild)
        id = await channel.send("Loading Data")
        info = {}
        f = open("./missions/"+data[0])
        info = json.loads(f.read())
        f.close()
        info['id'] = id.id
        f = open("./missions/"+data[0],'w')
        f.write(json.dumps(info, indent=4, sort_keys=True))
        f.close()
        await self.displayEvent(message.channel.guild, data[0], id)

    async def refresh(self, data, client, message):
        channel = self.getEventChannel(message.channel.guild)
        async for log in channel.history(limit=5):
            if log.content.startswith("|EVENT"):
                lines = log.content.split("\n")
                fname = lines[0].split(": ")[1][:-1]
                await self.displayEvent(message.channel.guild, fname, id)
                return

    def getEventChannel(self, guild):
        for c in guild.channels:
            if c.name.lower() == "events":
                return c
        return None

    async def displayEvent(self, guild, event, message):
        with open("./missions/"+event) as f:
            data = json.loads(f.read())
            slots = "__Slots:__\n\n"
            for s in data['slots']:
               slots += "\n**"+s['name']+"**\n\n"
               for r in s['slots']:
                   slots += "    " + r['name'] + ": "
                   if "player" in r:
                       slots += "**"+r['player']+"**\n"
                   else:
                       slots += "\n"
            await message.edit(content="|EVENT: "+event+"|\n\n**"+data['name']+"**\n\n"+"__Date__: "+data['date']+"\n__Map:__ "+data['map']+"\n\n"+data['desc']+"\n\n"+slots+"\n")

    async def savePost(self, fname, post):
        f = open("./missions/"+fname,'w')
        f.write(json.dumps(post, indent=4, sort_keys=True))
        f.close()
