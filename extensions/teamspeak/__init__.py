"""TeamSpeak Utilities"""
import argparse
import discord

class BotExtension:
    """TeamSpeak Utilities"""
    def __init__(self, bot):
        self.name = "TeamSpeak IP"
        self.author = "Brett"
        self.version = "1.1"
        self.bot = bot


    def __register__(self):
        return {
            "ts" : {
                "function" : self.teamspeak,
                "roles" : ["active"]
            }
        }

    async def teamspeak(self, args, message):
        """"Send the TeamSpeak Address to a user"""
        parser = argparse.ArgumentParser(description=self.teamspeak.__doc__)
        parser.add_argument("user", help="The user to send the address to")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            try:
                user = message.channel.guild.get_member(self.bot.get_from_tag(args.user))
                await user.send("The TeamSpeak address is ts.synixe.com")
                await message.channel.send("Sent 👍")
            except AttributeError:
                await message.channel.send("I'm not sure who that is...")

    async def on_message(self, message):
        """Don't let the TS address be posted in Discord"""
        if message.author.id != self.bot.user.id:
            if "ts.synixe.com" in message.content.lower():
                await message.channel.send("Please don't post the TeamSpeak Address. Instead an @Active member needs to use `?ts [user]` to send someone the TeamSpeak address.")
                await message.delete()
