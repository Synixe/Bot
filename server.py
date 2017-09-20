import discord

SERVERS = {"arma3":"Primary Arma 3"}

class Commands():
    def register(self, _):
        return {
            "start" : {
                "function" : self.start,
                "description" : "Start ",
                "roles" : ["manager"]
            }
        }

    async def start(self, data, client, message):
        if data[0].lower() not in SERVERS:
            await message.channel.send("Unknown Server")
        else:
            await message.channel.send("Unable to start: "+SERVERS[data[0].lower()])
