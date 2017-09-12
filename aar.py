import pymysql
import discord
import asyncio
import tokens

class Commands():
    def register(self, client):
        self.mission_loop = client.loop.create_task(self.mission_loop_task(client))
        return {}

    async def mission_loop_task(self, client):
        await client.wait_until_ready()
        db = pymysql.connect("ts.synixe.com","r3",tokens.getToken("mysql"),"r3")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM `replays` WHERE `hidden` = '0' ORDER BY `id` DESC LIMIT 1")
        data = cursor.fetchone()
        f = open("aar")
        last = f.read().strip().split("|")
        last[0] = int(last[0])
        f.close()
        if last[0] != data[0]:
            if data[5] == None and last[1] != "progress":
                f = open("aar","w")
                f.write(str(data[0])+"|progress")
                f.close()
            else:
                f = open("aar","w")
                f.write(str(data[0])+"|done")
                f.close()
                for guild in client.guilds:
                    if "synixe" in guild.name.lower():
                        for c in guild.channels:
                            if c.name.lower() == "postop":
                                await c.send("AAR for "+data[1]+"\nhttp://ts.synixe.com/arma3-aar/"+data[7]+"/"+data[2])
        else:
            if last[1] == "progress" data[5] != None:
                f = open("aar","w")
                f.write(str(data[0])+"|done")
                f.close()
                for guild in client.guilds:
                    if "synixe" in guild.name.lower():
                        for c in guild.channels:
                            if c.name.lower() == "postop":
                                await c.send("AAR for "+data[1]+"\nhttp://ts.synixe.com/arma3-aar/"+data[7]+"/"+data[2])
