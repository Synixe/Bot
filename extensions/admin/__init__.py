"""Admin Utilites"""
import argparse
import random
import logger
import sys
import discord

class BotExtension:
    """Admin Utilites"""
    def __init__(self, bot):
        self.name = "Admin Tools"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def __register__(self):
        return {
            "clear" : {
                "function" : self.clear,
                "roles" : ["manager"]
            },
            "ext" : {
                "function" : self.ext,
                "roles" : ["@everyone"]
            },
            "freeze" : {
                "function" : self.freeze,
                "roles" : ["manager", "moderator"]
            },
            "unfreeze" : {
                "function" : self.unfreeze,
                "roles" : ["manager", "moderator"]
            },
            "speak" : {
                "function" : self.speak,
                "roles" : ["manager"]
            },
            "anon" : {
                "function" : self.anon,
                "roles" : ["@everyone"]
            }
        }

    async def clear(self, args, message):
        """Clears the past n number of messages (Default: 20)"""
        parser = argparse.ArgumentParser(description=self.clear.__doc__)
        parser.add_argument(
            "n", nargs="?", default=20, type=int,
            help="The number of messages to delete, default: 20"
        )
        parser.add_argument("--pinned", action="store_true", help="Delete pinned messages")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            messages = message.channel.history(limit=args.n + 2)
            status = await message.channel.send("Clearing {0} messages".format(args.n + 2))
            remaining = args.n + 2
            async for log in messages:
                if args.pinned or not log.pinned:
                    try:
                        if log.id != status.id:
                            await log.delete()
                    except discord.errors.NotFound:
                        logger.error("Failed to delete a message during clear.")
                remaining -= 1
                try:
                    await status.edit(content="Clearing {0} messages".format(remaining))
                except discord.errors.NotFound:
                    #Chances are 2 clear functions are running, stop this one
                    return
            await status.delete()

    async def freeze(self, args, message):
        """Freeze a user from sending messages"""
        parser = argparse.ArgumentParser(description=self.freeze.__doc__)
        parser.add_argument("user", help="The user to freeze")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            user = message.channel.guild.get_member(self.bot.get_from_tag(args.user))
            if user != None:
                if self.bot.in_role_list(user, ["manager"]):
                    #async with message.channel.typing():
                    #    await message.channel.send(file=discord.File(fp=gifs.getRandom("treason")))
                    await message.channel.send(":laughing:")
                else:
                    await user.add_roles(self.getRole(message.channel.guild,"Silenced"))
                    await message.channel.send("Froze {0.display_name}".format(user))
            else:
                await message.channel.send("Can't find that user.")

    async def unfreeze(self, args, message):
        """"Unfreeze a user from sending messages"""
        parser = argparse.ArgumentParser(description=self.unfreeze.__doc__)
        parser.add_argument("user", help="The user to unfreeze")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            user = message.channel.guild.get_member(self.bot.get_from_tag(args.user))
            if user != None:
                await user.remove_roles(self.getRole(message.channel.guild,"Silenced"))
                await message.channel.send("Unfroze {0.display_name}".format(user))
            else:
                await message.channel.send("Can't find that user.")

    async def ext(self, args, message):
        """Get info about loaded extensions"""
        parser = argparse.ArgumentParser(description=self.ext.__doc__)
        parser.add_argument("extension", nargs="?", type=str, help="The extension to get info about")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            if args.extension == None:
                embed = discord.Embed(
                    title = self.bot.user.display_name,
                    description = ", ".join(self.bot.extension_list)
                )
                embed.set_footer(text="Use ?ext [module] to see commands and handlers.")
                embed.add_field(name="Commands", value=self.bot._num_commands)
                embed.add_field(name="Handlers", value=self.bot._num_handlers)
                embed.add_field(name="Loops",  value=self.bot._num_loops)
                await message.channel.send(embed=embed)
            else:
                if args.extension in self.bot.extension_list:
                    if hasattr(self.bot.extensions[args.extension],"active"):
                        if not self.bot.extensions[args.extension].active:
                            color = discord.Colour.from_rgb(r=255, g=0, b=0)
                        else:
                            color = discord.Colour.from_rgb(r=0, g=255, b=0)
                    else:
                        color = discord.Colour.from_rgb(r=0, g=255, b=0)
                    embed = discord.Embed(
                        title = "{0.name} v{0.version} by {0.author}".format(self.bot.extensions[args.extension]),
                        color = color
                    )
                    if args.extension in self.bot._ext_handlers:
                        embed.add_field(
                            name="Handlers",
                            value=", ".join(self.bot._ext_handlers[args.extension])
                        )
                    if args.extension in self.bot._ext_loops:
                        embed.add_field(
                            name="Loops",
                            value=", ".join(self.bot._ext_loops[args.extension])
                        )
                    if args.extension in self.bot._ext_commands:
                        description = ""
                        for name, c in self.bot._ext_commands[args.extension].items():
                            description += name+"\n"
                            description += "    "+c['description']+"\n"
                        await message.channel.send(
                            embed=embed,
                            content="```\n"+description+"```"
                        )
                    else:
                        await message.channel.send(embed=embed)
                else:
                    await message.channel.send("That extension does not exist.")

    async def speak(self, args, message):
        """"Makes the bot say something funny"""
        parser = argparse.ArgumentParser(description=self.speak.__doc__)
        parser.add_argument("channel", help="The channel")
        parser.add_argument("words", nargs="+", type=str)
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            channel = discord.utils.find(lambda c: c.name == args.channel, message.channel.guild.channels)
            if channel is not None:
                await channel.send(" ".join(args.words))

    async def anon(self, args, message):
        """Send a message to the Moderators anonymously"""
        if not isinstance(message.channel, discord.DMChannel):
            await message.delete()
            await message.channel.send("Only use this command in a direct message.")
        else:
            channel = discord.utils.find(lambda c: c.name == "inbox", discord.utils.find(lambda g: g.name == "Synixe", self.bot.guilds).channels)
            if channel is not None:
                await channel.send(" ".join(args))
                await message.channel.send("Message sent!")

    @classmethod
    def getRole(cls, guild, name):
        """File a role by name"""
        for role in guild.roles:
            if name.lower() == role.name.lower():
                return role
        return None

    async def on_message(self, message):
        """Send `Allegedly` for 1\% of Brett's Messages"""
        if message.author.id == 307524009854107648:
            if random.random() < 0.01:
                await message.channel.send("Allegedly...")
