import discord

class Commands():
    def register(self, _):

        return {
            "poll" : {
                "function" : self.poll,
                "description" : "Create a quick poll",
                "roles" : ["manager"]
            }
        }

    async def poll(self, data, client, message):
        await message.channel.send(data[0])
        await message.channel.send(client.getIDFromTag(data[0]))
