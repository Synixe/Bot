"""Git Information from Discord"""
import argparse
import subprocess
import discord
import os

from . import blame

class BotExtension:
    """Git Information from Discord"""
    def __init__(self, bot):
        self.bot = bot
        self.name = "Git"
        self.author = "Brett"
        self.version = "1"

    def __register__(self):
        return {
            "current" : {
                "function": self.current,
                "roles" : ["@everyone"]
            },
            "blame" : {
                "function": self.blame,
                "roles" : ["@everyone"]
            },
            "update" : {
                "function": self.update,
                "roles" : ["code contributer"]
            },
            "log" : {
                "function": self.log,
                "roles" : ["code contributer"]
            }
        }

    def __loops__(self):
        return {
            "update-check" : self.bot.loop.create_task(self.update_task())
        }

    async def update_task(self):
        await self.bot.wait_until_ready()
        if os.path.isfile("/tmp/restart-synixe-bot"):
            with open("/tmp/restart-synixe-bot") as f:
                data = f.read().split("|")
            channel = self.bot.get_channel(int(data[0]))
            message = await channel.get_message(int(data[1]))
            await message.edit(embed=discord.Embed(title="Restarted! Current Commit: {}".format(subprocess.getoutput("git log --pretty=format:'%h' -n 1")),color=discord.Color.from_rgb(r=0,g=255,b=0)))

    async def current(self, args, message):
        """Find out which commit the bot is on"""
        embed = discord.Embed(
            title=subprocess.getoutput("git log --pretty=format:'%h' -n 1"),
            url="https://github.com/Synixe/Bot/commit/" + subprocess.getoutput("git log --pretty=format:'%H' -n 1").strip("'"),
            color=discord.Colour.from_rgb(r=255, g=192, b=60)
        )
        embed.add_field(name="Last Change", value=subprocess.getoutput("git log -1 --pretty=format:'%an'").strip("'").split(" ")[0])
        embed.add_field(name="Title", value=subprocess.getoutput("git log -1 --pretty=%B"), inline=False)
        await message.channel.send(embed=embed)

    async def blame(self, args, message):
        """Find out who wrote a command"""
        parser = argparse.ArgumentParser(blame.__doc__)
        parser.add_argument("command", help="The command to blame")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            for ext in self.bot.extensions:
                if hasattr(self.bot.extensions[ext], args.command):
                    authors, start, end = blame.blame(ext, args.command)
                    if isinstance(authors, str):
                        await message.channel.send(authors)
                        return
                    total = 0
                    for author in authors:
                        total += authors[author]
                    embed = discord.Embed(
                        title=self.bot.prefix+args.command,
                        url="https://github.com/Synixe/Bot/blob/rewrite/extensions/"+ext+"/__init__.py#L"+str(start)+"L"+str(end),
                        color=discord.Colour.from_rgb(r=255, g=192, b=60)
                    )
                    embed.add_field(name="Lines", value="{}".format(total), inline=False)
                    for author in authors:
                        embed.add_field(name=author, value="{} Lines ({}%)".format(
                            authors[author], round(authors[author] / total * 100, 0))
                        )
                    await message.channel.send(embed=embed)

    async def update(self, args, message):
        """Update the Bot and restart"""
        subprocess.getoutput("git pull")
        mid = await message.channel.send(embed=discord.Embed(title="Restarting",color=discord.Color.from_rgb(r=255,g=255,b=0)))
        with open("/tmp/restart-synixe-bot",'w') as f:
            f.write(str(message.channel.id)+"|"+str(mid.id))
        os.system("sudo systemctl restart synixebot")

    async def log(self, args, message):
        """Get the bot log"""
        with open("./bot.log", encoding="utf-8") as log:
          await message.channel.send("```\n"+log.read()+"\n```")
