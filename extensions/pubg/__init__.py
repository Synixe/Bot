import argparse
import urllib.request
import discord
import sys
from . import pubgparser

class BotExtension:
    def __init__(self, bot):
        self.name = "PLAYER UNKNOWN's Battlegrounds"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def register(self):
        return {
            "pubg" : {
                "function" : self.pubg,
                "description" : "Display PLAYER UNKNOWN's Battlegrounds stats",
                "roles" : ["@everyone"]
            }
        }

    async def pubg(self, args, message):
        async with message.channel.typing():
            parser = argparse.ArgumentParser(description="Display PLAYER UNKNOWN's Battlegrounds stats")
            parser.add_argument("user", help="The PUBG username you want to fetch")
            parser.add_argument("-m", dest="mode", help="Game Mode",choices=["lifetime","solo","duo","squad","solo-fpp","duo-fpp","squad-fpp"],default="Lifetime")
            args = parser.parse_args(args)
            args.user = args.user.lower()
            parser = pubgparser.PUBGParser()
            platform = "pc"
            parser.check_next = False
            req = urllib.request.Request(url="https://pubgtracker.com/profile/"+platform+"/"+args.user,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
            with urllib.request.urlopen(req) as response:
                parser.feed(response.read().decode("UTF-8"))
            try:
                parser.process()
            except:
                await message.channel.send("I wasn't able to find that player!")
                return
            embed = discord.Embed(
                title = parser.data['PlayerName'],
                url = "https://pubgtracker.com/profile/"+platform+"/"+parser.data['PlayerName'].strip()
            )
            mode = args.mode.lower()
            if len(parser.data[mode]) != 0:
                embed.add_field(name="Kills",value=parser.data[mode]["Kills"],inline=True)
                embed.add_field(name="Matches Played",value=parser.data[mode]["Rounds Played"],inline=True)
                embed.add_field(name="Wins",value=parser.data[mode]["Wins"],inline=True)
                embed.add_field(name="Top 10s",value=parser.data[mode]["Top 10s"],inline=True)
            else:
                embed.description = "This player has not played "+args.mode
            embed.set_thumbnail(url=parser.data["Avatar"])
            await message.channel.send(embed=embed)
