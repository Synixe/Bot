import discord

class Commands():
    def register(self, _):

        return {
            "runas" : {
                "function" : self.runas,
                "description" : "Run a command as a different user",
                "roles" : ["manager"]
            },
            "clear" : {
                "function" : self.clear,
                "description" : "Clear the 100 most recent message from the current channel",
                "roles" : ["manager"]
            }
        }

    async def runas(self, data, client, message):
        try:
            user = message.channel.guild.get_member(int(data[0]))
        except:
            await message.channel.send("Unable to find that user.")
            return
        message.author = user
        message.content = " ".join(data[1:])
        await message.channel.send("Executing as "+user.display_name)
        await client.execute(message)

    async def clear(self, data, client, message):
        async for log in message.channel.history(limit=100):
            await log.delete()
