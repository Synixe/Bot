"""Pack of small commands"""
import argparse
import random
import discord
import logger

class BotExtension:
    """Pack of small commands"""
    def __init__(self, bot):
        self.name = "Mini Commands"
        self.author = "Brett + nameless"
        self.version = "1.4"
        self.bot = bot

    def __register__(self):
        return {
            "card" : {
                "function" : self.card,
                "roles" : ["active", "new", "inactive"]
            },
            "ping" : {
                "function" : self.ping,
                "roles" : ["@everyone"]
            },
            "color" : {
                "function" : self.color,
                "roles" : ["active", "new", "inactive"],
                "alias": ["colour"]
            },
            "avatar" : {
                "function" : self.avatar,
                "roles" : ["active", "new", "inactive"]
            }
        }

    async def card(self, args, message):
        """Display a card with information about a member"""
        parser = argparse.ArgumentParser(self.card.__doc__)
        parser.add_argument("user", nargs="?", default=str(message.author.id), help="The subject of the card. Defaults to the message's author.")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            user = message.channel.guild.get_member(self.bot.get_from_tag(args.user))
            if user != None:
                embed = discord.Embed(
                    title=user.name,
                    color=user.colour
                )
                embed.add_field(name="Joined on", value=user.joined_at.strftime("%B %d, %Y"))
                embed.set_thumbnail(url=user.avatar_url)
                await message.channel.send(embed=embed)
            else:
               await message.channel.send("Unable to find that user. Try using @ to mention them or use their Discord ID.")

    async def ping(self, args, message):
        """Ping the bot for a response"""
        parser = argparse.ArgumentParser(description=self.ping.__doc__)
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            await message.channel.send("{:0.0f}ms".format(self.bot.latency * 1000))

    async def color(self, args, message):
        """Obtain the color of a role on the server"""
        parser = argparse.ArgumentParser(description=self.color.__doc__)
        parser.add_argument("role", nargs="?+", default=[str(message.author.roles[-1].name)], help="The role to get the color of")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            args.role = " ".join(args.role)
            role = discord.utils.find(lambda m: m.name.lower() == args.role.lower(), message.channel.guild.roles)
            if role != None:
                embed = discord.Embed(
                    title=role.name,
                    color=role.colour
                )
                embed.add_field(name="RGB", value="{0.r}, {0.g}, {0.b}".format(role.color))
                embed.add_field(name="Hex", value=str(role.color))
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Role not found")

    async def avatar(self, args, message):
        """Prints out a users discord avatar"""
        parser = argparse.ArgumentParser(description=self.avatar.__doc__)
        parser.add_argument("avatar", nargs="?", default=str(message.author.id), help="The user of the avatar you want to get")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            user = message.channel.guild.get_member(self.bot.get_from_tag(args.avatar))
            if user != None:
                embed = discord.Embed(
                    color=user.color
                )
                embed.set_author(
                    name=user.name,
                    url=user.avatar_url
                )
                embed.set_image(url=user.avatar_url)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("User not found")
