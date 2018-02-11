import argparse
import discord

class BotExtension:
    def __init__(self, bot):
        self.name = "Mini Commands"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot


    def register(self):
        return {
            "ts" : {
                "function" : self.ts,
                "description" : "Send the TeamSpeak Address to a user",
                "roles" : ["active"]
            }
        }

    async def ts(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Send the TeamSpeak Address to a user", message))
        parser.add_argument("user",help=self.bot.processOutput("The user to send the address to", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            try:
                user = message.channel.guild.get_member(self.bot.getIDFromTag(args.user))
                await user.send("The TeamSpeak address is ts.synixe.com")
            except AttributeError:
                await message.channel.send("I'm not sure who that is...")

    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            if "ts.synixe.com" in message.content:
                await message.channel.send("Please don't post the TeamSpeak Address. Instead an @Active member needs to use `?ts [user]` to send someone the address.")
                await message.delete()
