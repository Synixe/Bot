import discord
import argparse
import subprocess

from . import blame

class BotExtension:
    def __init__(self, bot):
        self.bot = bot
        self.name = "Git"
        self.author = "Brett"
        self.version = "1"

    def register (self):
        return {
            "current" : {
                "function": self.current,
                "roles" : ["@everyone"]
            },
            "blame" : {
                "function": self.blame,
                "roles" : ["@everyone"]
            }
        }

    async def current(self, args, message):
        """Find out which commit the bot is on"""
        embed = discord.Embed(
            title = subprocess.getoutput("git log --pretty=format:'%h' -n 1"),
            url = "https://github.com/Synixe/Bot/commit/" + subprocess.getoutput("git log --pretty=format:'%H' -n 1"),
            color = discord.Colour.from_rgb(r=255,g=192,b=60)
        )
        embed.add_field(name="Last Change",value=subprocess.getoutput("git log -1 --pretty=format:'%an'"))
        embed.add_field(name="Title",value=subprocess.getoutput("git log -1 --pretty=%B"), inline=False)
        await message.channel.send(embed=embed)

    async def blame(self, args, message):
        """Find out who wrote a command"""
        parser = argparse.ArgumentParser(blame.__doc__)
        parser.add_argument("command",help="The command to blame")
        args = await self.bot.parseArgs(parser, args, message)
        for ext in self.bot.extensions:
            if hasattr(self.bot.extensions[ext], args.command):
                authors, start, end = blame.blame(ext, args.command)
                if isinstance(authors, str):
                    await message.channel.send(authors)
                    return
                total = 0
                for a in authors:
                    total += authors[a]
                embed = discord.Embed(
                    title = self.bot.prefix+args.command,
                    url = "https://github.com/Synixe/Bot/blob/rewrite/extensions/"+ext+"/__init__.py#L"+str(start)+"L"+str(end),
                    color = discord.Colour.from_rgb(r=255,g=192,b=60)
                )
                embed.add_field(name="Lines",value="{}".format(total), inline=False)
                for a in authors:
                    embed.add_field(name=a,value="{} Lines ({}%)".format(authors[a], round(authors[a] / total * 100, 0)))
                await message.channel.send(embed=embed)
