"""Role Counter"""
import argparse
import discord
import logger

class BotExtension:
    """Role Counter"""
    def __init__(self, bot):
        self.name = "Roles Command"
        self.author = "nameless + Brett"
        self.version = "1.1"
        self.bot = bot

    def __register__(self):
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
        parser.add_argument(
            "--list",
            nargs="+",
            help="Get list of members (names) with that role"
        )
        parser.add_argument("--sort", help="Attribute to sort by",
            choices=["join", "name"],
            default="name"
        )
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            active = len(self.get_members_with_role(message.channel.guild, "active"))
            new    = len(self.get_members_with_role(message.channel.guild, "new"))
            if args.total: #count --total
                embed = discord.Embed(
                    title = "Active + New Members",
                    color = discord.Colour.from_rgb(r=255, g=192, b=60)
                )
                embed.add_field(name="Total",   value="{}".format(active+new))
                embed.add_field(name="Active",  value="{}".format(active))
                embed.add_field(name="New",     value="{}".format(new))
            elif args.list != None: #count --list [list]
                members = self.get_members_with_role(message.channel.guild, " ".join(args.list))
                if len(members) == 0:
                    await message.channel.send("Role not found")
                    return
                if args.sort == "name":
                    members.sort(key=lambda x: x.display_name)
                elif args.sort == "join":
                    members.sort(key=lambda x: x.joined_at)
                embed = discord.Embed(
                    title="Members in {}".format(" ".join(args.list).title()),
                    color=discord.Colour.from_rgb(r=255, g=192, b=60),
                    description=", ".join(["<@{}>".format(m.id) for m in members])
                )
            else: #count
                inactive = len(self.get_members_with_role(message.channel.guild, "inactive"))
                embed = discord.Embed(
                    title="Members with Activity Roles",
                    color=discord.Colour.from_rgb(r=255, g=192, b=60)
                )
                embed.add_field(name="Active",   value="{}".format(active))
                embed.add_field(name="New",      value="{}".format(new))
                embed.add_field(name="Inactive", value="{}".format(inactive))
            await message.channel.send(embed=embed)

    @classmethod
    def get_members_with_role(cls, guild, role):
        """Get the number of members with a certain role"""
        role = discord.utils.find(lambda r: r.name.lower() == role.lower(), guild.roles)
        members = [m for m in guild.members if role in m.roles]
        return members
