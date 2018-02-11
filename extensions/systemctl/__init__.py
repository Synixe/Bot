import argparse
import discord
import subprocess
import os
import asyncio

class BotExtension:
    def __init__(self, bot):
        self.name = "System Control"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

        self.services = {"arma" : {"name": "Arma 3 Dedicated Server", "unit": "arma3-mod"}}

    def register(self):
        return {
            "status" : {
                "function" : self.status,
                "description" : "Get the status of a system service",
                "roles" : ["moderator","manager"]
            },
            "start" : {
                "function" : self.start,
                "description" : "Start a service",
                "roles" : ["moderator","manager"]
            }
        }

    async def status(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Get the status of a system service", message))
        parser.add_argument("service", help=self.bot.processOutput("The systemctl service", message))
        parser.add_argument("--full",action="store_true",help=self.bot.processOutput("Display the full status", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            if args.service in self.services:
                if args.full:
                    r = subprocess.run(["systemctl","status",self.services[args.service]["unit"]], stdout=subprocess.PIPE)
                    with open("status.log","w") as f:
                        f.write(r.stdout.decode("UTF-8"))
                    await message.channel.send("```\n"+"\n".join(r.stdout.decode("UTF-8").split("\n")[0:11])+"\n```")
                    await message.channel.send("```\n"+"\n".join(r.stdout.decode("UTF-8").split("\n")[12:])+"\n```")
                else:
                    r = subprocess.run(["systemctl","is-active",self.services[args.service]["unit"]], stdout=subprocess.PIPE)
                    if r.stdout.decode("UTF-8")[:-1] == "active":
                        color = discord.Colour.from_rgb(r=0,g=255,b=0)
                        description = "Active"
                    else:
                        color = discord.Colour.from_rgb(r=255,g=0,b=0)
                        description = "Inactive"
                    embed = discord.Embed(
                        title = self.services[args.service]["name"],
                        color = color,
                        description = self.bot.processOutput(description, message)
                    )
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("Unknown Service")

    async def start(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Start a service", message))
        parser.add_argument("service",help=self.bot.processOutput("The systemctl service", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            if args.service in self.services:
                r = subprocess.run(["systemctl","is-active",self.services[args.service]["unit"]], stdout=subprocess.PIPE)
                if r.stdout.decode("UTF-8")[:-1] == "active":
                    embed = discord.Embed(
                        title = self.services[args.service]["name"],
                        color = discord.Colour.from_rgb(r=0,g=255,b=0),
                        description = self.bot.processOutput("Already Active", message)
                    )
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title = self.services[args.service]["name"],
                        color = discord.Color.from_rgb(r=255,g=255,b=0),
                        description = self.bot.processOutput("Starting...", message)
                    )
                    holder = await message.channel.send(embed=embed)
                    os.system("sudo systemctl start "+self.services[args.service]["unit"])
                    await asyncio.sleep(20)
                    r = subprocess.run(["systemctl","is-active",self.services[args.service]["unit"]], stdout=subprocess.PIPE)
                    if r.stdout.decode("UTF-8")[:-1] == "active":
                        embed = discord.Embed(
                            title = self.services[args.service]["name"],
                            color = discord.Colour.from_rgb(r=0,g=255,b=0),
                            description = self.bot.processOutput("Active", message)
                        )
                    else:
                        embed = discord.Embed(
                            title = self.services[args.service]["name"],
                            color = discord.Colour.from_rgb(r=255,g=0,b=0),
                            description = self.bot.processOutput("Inactive", message)
                        )
                    await holder.edit(embed=embed)
            else:
                await message.channel.send("Unknown Service")
