import argparse
import urllib.request
import discord
import sys
from . import r6parser

class BotExtension:
    def __init__(self, bot):
        self.name = "Rainbow 6 Siege"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def register(self):
        return {
            "r6" : {
                "function" : self.r6,
                "description" : "Display Rainbow 6 Siege stats",
                "roles" : ["@everyone"]
            }
        }

    async def r6(self, args, message):
        async with message.channel.typing():
            parser = argparse.ArgumentParser(description=self.bot.processOutput("Display Rainbow 6 Siege stats", message))
            parser.add_argument("user", help=self.bot.processOutput("The Rainbow 6 Siege username you want to fetch", message))
            parser.add_argument("--psn", help=self.bot.processOutput("Search for a PSN account", message),action="store_true")
            parser.add_argument("--xbox", help=self.bot.processOutput("Search for a Xbox account", message),action="store_true")
            args = parser.parse_args(args)
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
            req = urllib.request.Request(url="https://r6.tracker.network/profile/"+platform+"/"+args.user,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
            try:
                with urllib.request.urlopen(req) as response:
                    parser.feed(response.read().decode("UTF-8"))
                embed = discord.Embed(
                    title = parser.name,
                    url = "http://r6.tracker.network/profile/"+platform+"/"+parser.name.strip()
                )
                embed.add_field(name=self.bot.processOutput("Kills", message),value=parser.kills,inline=True)
                embed.add_field(name=self.bot.processOutput("Deaths", message),value=parser.deaths,inline=True)
                embed.add_field(name=self.bot.processOutput("W/L", message),value=parser.wlr,inline=True)
                embed.add_field(name=self.bot.processOutput("Accuracy", message),value=parser.accuracy,inline=True)
                if (parser.profile != None):
                    embed.set_thumbnail(url=parser.profile)
                await message.channel.send(embed=embed)
            except:
                await message.channel.send(self.bot.processOutput("I wasn't able to find that player!", message))
