"""Control Systemd Units from Discord"""
import argparse
import subprocess
import os
import asyncio
import discord

class BotExtension:
    """Control Systemd Units from Discord"""
    def __init__(self, bot):
        self.name = "System Control"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot
        self.disable_during_test = True

        self.services = {"arma" : {"name": "Arma 3 Dedicated Server", "unit": "arma3-mod"}}

    def __register__(self):
        return {
            "status" : {
                "function" : self.status,
                "roles" : ["moderator", "manager"]
            },
            "start" : {
                "function" : self.start,
                "roles" : ["moderator", "manager"]
            }
        }

    async def status(self, args, message):
        """Get the status of a system service"""
        parser = argparse.ArgumentParser(description=self.status.__doc__)
        parser.add_argument("service", help="The systemctl service")
        parser.add_argument("--full", action="store_true", help="Display the full status")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            if args.service in self.services:
                if args.full:
                    status = subprocess.run(
                        ["systemctl", "status", self.services[args.service]["unit"]],
                        stdout=subprocess.PIPE
                    )
                    with open("status.log", "w") as log:
                        log.write(status.stdout.decode("UTF-8"))
                    await message.channel.send("```\n"+"\n".join(status.stdout.decode("UTF-8").split("\n")[0:11])+"\n```")
                    await message.channel.send("```\n"+"\n".join(status.stdout.decode("UTF-8").split("\n")[12:])+"\n```")
                else:
                    r = subprocess.run(
                        ["systemctl", "is-active", self.services[args.service]["unit"]],
                        stdout=subprocess.PIPE
                    )
                    if r.stdout.decode("UTF-8")[:-1] == "active":
                        color = discord.Colour.from_rgb(r=0, g=255, b=0)
                        description = "Active"
                    else:
                        color = discord.Colour.from_rgb(r=255, g=0, b=0)
                        description = "Inactive"
                    embed = discord.Embed(
                        title=self.services[args.service]["name"],
                        color=color,
                        description=description
                    )
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("Unknown Service")

    async def start(self, args, message):
        """Start a service"""
        parser = argparse.ArgumentParser(description=self.start.__doc__)
        parser.add_argument("service", help="The systemctl service")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            if args.service in self.services:
                if self.is_active(self.services[args.service]["unit"]):
                    embed = self.unit_embed(
                        self.services[args.service]["name"],
                        discord.Colour.from_rgb(r=0, g=255, b=0),
                        "Already Active"
                    )
                    await message.channel.send(embed=embed)
                else:
                    embed = self.unit_embed(
                        self.services[args.service]["name"],
                        discord.Color.from_rgb(r=255, g=255, b=0),
                        "Starting..."
                    )
                    holder = await message.channel.send(embed=embed)
                    os.system("sudo systemctl start "+self.services[args.service]["unit"])
                    await asyncio.sleep(20)
                    if self.is_active(self.services[args.service]["unit"]):
                        embed = self.unit_embed(
                            self.services[args.service]["name"],
                            discord.Colour.from_rgb(r=0, g=255, b=0),
                            "Active"
                        )
                    else:
                        embed = self.unit_embed(
                            self.services[args.service]["name"],
                            discord.Colour.from_rgb(r=255, g=0, b=0),
                            "Inactive"
                        )
                    await holder.edit(embed=embed)
            else:
                await message.channel.send("Unknown Service")

    @classmethod
    def unit_embed(cls, title, text, color):
        """Wrapper for creating embed, can probably be removed"""
        return discord.Embed(title=title, color=color, description=text)

    @classmethod
    def is_active(cls, unit):
        """Checks if a unit is active"""
        subprocess.run(
            ["systemctl","is-active",self.services[args.service]["unit"]],
            stdout=subprocess.PIPE
        )
        return is_active.stdout.decode("UTF-8")[:-1] == "active"
