import discord
import requests
import json
import asyncio
import pymysql

import certs
import tokens

AAR_FILE = "./data/aar.txt"

class Commands():
    def register(self, client):
        self.client = client
        # AAR DISABLED - self.mission_loop = client.loop.create_task(self.mission_loop_task(client))
        return {
            "missionup" : {
                "function" : self.missionup,
                "description" : "Upload a mission to the server",
                "roles" : ["missionmaker"]
            },
            "eventup" : {
                "function" : self.eventup,
                "description" : "Upload an event sheet to the server",
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

    async def mission_loop_task(self, client):
        await client.wait_until_ready()
        while not client.is_closed():
            print("Checking AAR")
            db = pymysql.connect("ts.synixe.com","r3",tokens.getToken("mysql"),"r3")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM `replays` WHERE `hidden` = '0' ORDER BY `id` DESC LIMIT 1")
            data = cursor.fetchone()
            cursor.close()
            db.close()
            f = open(AAR_FILE)
            last = f.read().strip().split("|")
            last[0] = int(last[0])
            f.close()
            if last[0] != data[0]:
                if data[5] == None:
                    f = open(AAR_FILE ,"w")
                    f.write(str(data[0])+"|progress")
                    f.close()
                else:
                    f = open(AAR_FILE ,"w")
                    f.write(str(data[0])+"|done")
                    f.close()
                    await client.getGuild("synixe").getChannel("postop").send("AAR for "+data[1]+"\nhttp://ts.synixe.com/arma3-aar/"+data[7]+"/"+data[2])
            else:
                if last[1] == "progress" and data[5] != None:
                    f = open(AAR_FILE ,"w")
                    f.write(str(data[0])+"|done")
                    f.close()
                    await client.getGuild("synixe").getChannel("postop").send("AAR for "+data[1]+"\nhttp://ts.synixe.com/arma3-aar/"+data[7]+"/"+data[2])
            await asyncio.sleep(60)

    async def missionup(self, data, client, message):
        for attach in message.attachments:
            id = await message.channel.send("Downloading "+attach.filename)
            with open("/opt/steam/arma3-mods/mpmissions/"+attach.filename,'wb') as f:
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                f.write(requests.get(attach.url, headers=headers).content)
            await id.edit(content="Downloaded "+attach.filename)

    async def eventup(self, data, client, message):
        for attach in message.attachments:
            id = await message.channel.send("Downloading "+attach.filename)
            with open("/opt/slotbot/missions/"+attach.filename,'wb') as f:
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                f.write(requests.get(attach.url, headers=headers).content)
            await id.edit(content="Downloaded "+attach.filename)

    async def unslot(self, data, client, message):
        await self._unslot(message.channel.guild, message.author.id, message.channel)

    async def _unslot(self, guild, id, reply=None):
        f = open("./missions/"+self.getCurrentMission())
        post = json.loads(f.read())
        f.close()
        for s in post['slots']:
            for r in s['slots']:
                if "playerid" in r:
                    if str(r['playerid']) == str(id):
                        del r['playerid']
                        del r['player']
                        await self.savePost(self.getCurrentMission(), post)
                        if reply != None:
                            await reply.send("Unslotted :cry:")
                            await self.displayEvent(reply.guild, self.getCurrentMission())
                        return
        if reply != None:
            await reply.send("You were not slotted.")
        return

    async def slot(self, data, client, message):
        role = data[0]
        await self._unslot(message.channel.guild, message.author.id)
        f = open("./missions/"+self.getCurrentMission())
        post = json.loads(f.read())
        f.close()
        taken = False
        for s in post['slots']:
            for r in s['slots']:
                if role.lower() in r['name'].lower():
                    if "playerid" not in r:
                        if "requirement" in r:
                            qualified = certs.isQualified(message.author.id, r["requirement"])
                            if qualified and type(qualified) == bool:
                                user = message.channel.guild.get_member(int(message.author.id))
                                r['player'] = user.display_name
                                r['playerid'] = message.author.id
                                await message.channel.send("Slotted "+user.display_name+" into "+r['name'])
                                await self.savePost(self.getCurrentMission(),post)
                                await self.displayEvent(message.channel.guild, self.getCurrentMission())
                                return
                            else:
                                await message.channel.send("You are missing the following certifications: "+(", ".join(qualified)))
                                return
                        else:
                            r['player'] = message.author.display_name
                            r['playerid'] = message.author.id
                            await message.channel.send("Slotted "+message.author.display_name+" into "+r['name'])
                            await self.savePost(self.getCurrentMission(),post)
                            await self.displayEvent(message.channel.guild, self.getCurrentMission())
                            return
                    else:
                        taken = True
        if taken:
            await message.channel.send("No matching slots are free!")
        else:
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
        f = open("./missions/current",'w')
        f.write(data[0])
        f.close()
        await self.displayEvent(message.channel.guild, data[0], id)

    async def refresh(self, data, client, message):
        await self.displayEvent(message.channel.guild, self.getCurrentMission(), id)
        return

    def getCurrentMission(self):
        with open("missions/current") as f:
            return f.read().strip()

    def getEventChannel(self, guild):
        for c in guild.channels:
            if c.name.lower() == "events":
                return c
        return None

    async def displayEvent(self, guild, event, message = None):
        with open("./missions/"+event) as f:
            data = json.loads(f.read())
            embed = discord.Embed(
                title = data["name"],
                description = data["desc"],
                color = discord.Colour.from_rgb(r=255,g=192,b=60),
                url = data["url"] if "url" in data else None
            )
            if "host" in data:
                user = self.client.getGuild("synixe").get_member(int(data["host"]))
                embed.set_author(name=user.name,icon_url=user.avatar_url)
            if "image" in data:
                embed.set_image(url=data["image"])
            if "date" in data:
                embed.add_field(name="Date",value=data["date"])
            if "map" in data:
                embed.add_field(name="Map",value=data["map"])
            for squad in data['slots']:
                slots = ""
                for role in squad['slots']:
                    slots += role['name'] + ": "
                    if "player" in role:
                        slots += "**"+role['player']+"**\n"
                    else:
                        slots += "\n"
                embed.add_field(name=squad["name"],value=slots,inline=False)
            if message == None:
                message = await self.client.getChannel(self.client.getGuild("synixe"),"events").get_message(data["id"])
            await message.edit(content=None, embed = embed)

    async def savePost(self, fname, post):
        f = open("./missions/"+fname,'w')
        f.write(json.dumps(post, indent=4, sort_keys=True))
        f.close()
