import argparse
import discord
import logger

class BotExtension:
    def __init__(self, bot):
        self.name = "Roles Command"
        self.author = "nameless + Brett"
        self.version = "1.0"
        self.bot = bot

    def register(self):
        return {
            "count" : {
                "function" : self.count,
                "roles" : ["active","new","inactive"]
            }
        }

    async def count(self, args, message):
        """Displays a counter of how many members are on Active, New and Inactive"""
        parser = argparse.ArgumentParser(self.count.__doc__)
        args = await self.bot.parseArgs(parser, args, message)
        active      = self.getMembersWithRole(message.channel.guild, "active")
        new         = self.getMembersWithRole(message.channel.guild, "new")
        inactive    = self.getMembersWithRole(message.channel.guild, "inactive")
        embed = discord.Embed(
            title = "Members with Activity Roles",
            color = discord.Colour.from_rgb(r=255,g=192,b=60)
        )
        embed.add_field(name="Active",   value="{}".format(active))
        embed.add_field(name="New",      value="{}".format(new))
        embed.add_field(name="Inactive", value="{}".format(inactive))
        await message.channel.send(embed=embed)

    @classmethod
    def getMembersWithRole(cls, guild, role):
        role = discord.utils.find(lambda r: r.name.lower() == role.lower(), guild.roles)
        members = [m for m in guild.members if role in m.roles]
        return len(members)
