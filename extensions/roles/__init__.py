"""Role Counter"""
import argparse
import discord
import logger

class BotExtension:
    """Adds a Role Counter to the bot"""
    def __init__(self, bot):
        """Init with the bot object"""
        self.name = "Roles Command"
        self.author = "nameless + Brett"
        self.version = "1.0"
        self.bot = bot

    def register(self):
        """Register with the main bot"""
        return {
            "count" : {
                "function" : self.count,
                "roles" : ["active", "new", "inactive"]
            }
        }

    async def count(self, args, message):
        """Displays a counter of how many members are on
        Active, New and Inactive"""
        parser = argparse.ArgumentParser(self.count.__doc__)
        parser.add_argument(
            "--total",
            action="store_true",
            help="Get total number of active and new members"
        )
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            active = self.getMembersWithRole(message.channel.guild, "active")
            new    = self.getMembersWithRole(message.channel.guild, "new")
            if not args.total:
                inactive = self.getMembersWithRole(message.channel.guild, "inactive")
                embed = discord.Embed(
                    title="Members with Activity Roles",
                    color=discord.Colour.from_rgb(r=255, g=192, b=60)
                )
                embed.add_field(name="Active",   value="{}".format(active))
                embed.add_field(name="New",      value="{}".format(new))
                embed.add_field(name="Inactive", value="{}".format(inactive))
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title = "Active + New Members",
                    color = discord.Colour.from_rgb(r=255, g=192, b=60)
                )
                embed.add_field(name="Total",   value="{}".format(active+new))
                embed.add_field(name="Active",  value="{}".format(active))
                embed.add_field(name="New",     value="{}".format(new))
                await message.channel.send(embed=embed)

    @classmethod
    def getMembersWithRole(cls, guild, role):
        role = discord.utils.find(lambda r: r.name.lower() == role.lower(), guild.roles)
        members = [m for m in guild.members if role in m.roles]
        return len(members)
