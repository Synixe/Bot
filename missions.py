import discord

class Commands():
    def register(self, _):
        return {"hello" : self.hello}

    async def hello(self, data, client, message):
        print("Hello")
        await message.channel.send("Hello "+message.author.name)
