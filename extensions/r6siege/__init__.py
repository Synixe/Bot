import argparse
import urllib.request
import discord
import sys
from . import r6parser

class BotExtension:
    """Rainbow 6 Siege stats in Discord"""
    def __init__(self, bot):
        self.name = "Rainbow 6 Siege"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def __register__(self):
        return {
            "r6" : {
                "function" : self.rainbow6,
                "roles" : ["@everyone"]
            }
        }

    async def rainbow6(self, args, message):
        """Display Rainbow 6 Siege stats"""
        async with message.channel.typing():
            parser = argparse.ArgumentParser(description=self.r6.__doc__)
            parser.add_argument("user", help="The Rainbow 6 Siege username you want to fetch")
            parser.add_argument("--psn", help="Search for a PSN account", action="store_true")
            parser.add_argument("--xbox", help="Search for a Xbox account", action="store_true")
            args = await self.bot.parser_args(parser, args, message)
            if args != False:
                parser = r6parser.R6Parser()
                platform = "pc"
                if args.psn:
                    platform = "psn"
                elif args.xbox:
                    platform = "xbox"
                parser.kills = None
                parser.deaths = None
                parser.wlr = None
                parser.accuracy = None
                parser.profile = None
                parser.name = None
                req = urllib.request.Request(url="https://r6.tracker.network/profile/"+platform+"/"+args.user, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
                try:
                    with urllib.request.urlopen(req) as response:
                        parser.feed(response.read().decode("UTF-8"))
                    embed = discord.Embed(
                        title=parser.name,
                        url="http://r6.tracker.network/profile/"+platform+"/"+parser.name.strip()
                    )
                    embed.add_field(name="Kills", value=parser.kills, inline=True)
                    embed.add_field(name="Deaths", value=parser.deaths, inline=True)
                    embed.add_field(name="W/L", value=parser.wlr, inline=True)
                    embed.add_field(name="Accuracy", value=parser.accuracy, inline=True)
                    if parser.profile != None:
                        embed.set_thumbnail(url=parser.profile)
                    await message.channel.send(embed=embed)
                except urllib.error.HTTPError:
                    await message.channel.send("I wasn't able to find that player!")
