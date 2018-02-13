import argparse
import discord
import random

class BotExtension:
    def __init__(self, bot):
        self.name = "Mini Commands"
        self.author = "Brett + nameless"
        self.version = "1.3"
        self.bot = bot

    def register(self):
        return {
            "card" : {
                "function" : self.card,
                "description" : "Display a pretty card with information about a member",
                "roles" : ["active","new","inactive"]
            },
            "ping" : {
                "function" : self.ping,
                "description" : "Ping the bot for a response",
                "roles" : ["@everyone"]
            },
            "color" : {
                "function" : self.color,
                "description" : "Obtain the color of a role on the server",
                "roles" : ["active","new","inactive"]
            },
            "colour" : {
                "function" : self.color,
                "description" : "Obtain the color of a role on the server",
                "roles" : ["active","new","inactive"]
            },
            "avatar" : {
                "function" : self.avatar,
                "description" : "Prints out a users discord avatar",
                "roles" : ["active","new","inactive"]
            }
        }

    async def card(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Display a pretty card with information about a member", message))
        parser.add_argument("user", nargs="?", default=str(message.author.id), help=self.bot.processOutput("The subject of the card. Defaults to the message's author.", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            user = message.channel.guild.get_member(self.bot.getIDFromTag(args.user))
            if user != None:
                embed = discord.Embed(
                    title = user.name,
                    color = user.colour
                )
                embed.add_field(name=self.bot.processOutput("Joined on", message),value=user.joined_at.strftime("%B %d, %Y"))
                embed.set_thumbnail(url=user.avatar_url)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(self.bot.processOutput("Unable to find that user. Try using @ to mention them or use their Discord ID.", message))

    async def ping(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Ping the bot", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            await message.channel.send("{:0.0f}ms".format(self.bot.latency * 1000))

    async def color(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Obtain a colo(u)r from a role on the server", message))
        parser.add_argument("role", nargs="?", default=str(message.author.roles[-1].name), help=self.bot.processOutput("The role to get the color of", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            role = discord.utils.find(lambda m: m.name.lower() == args.role.lower(), message.channel.guild.roles)
            if role != None:
                embed = discord.Embed(
                    title = role.name,
                    color = role.colour
                )
                embed.add_field(name="RGB",value="{0.r}, {0.g}, {0.b}".format(role.color))
                embed.add_field(name="Hex",value=str(role.color))
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Role not found")

    async def avatar(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Shows an clickable avatar of a user", message))
        parser.add_argument("avatar", nargs="?", default=str(message.author.id), help=self.bot.processOutput("The user of the avatar you want to get", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            user = message.channel.guild.get_member(self.bot.getIDFromTag(args.avatar))
            if user != None:
                embed = discord.Embed(
                    color = user.color
                )
                embed.set_author(
                    name = user.name,
                    url = user.avatar_url
                )
                embed.set_image(url=user.avatar_url)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("User not found")
