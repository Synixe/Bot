"""Admin Utilites"""
import argparse
import random
import logger
import discord
import tokens

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
            },
            "runas": {
                "function" : self.runas,
                "roles" : ["manager","moderator","helper"]
            },
            "kick": {
                "function" : self.kick,
                "roles" : ["manager","moderator"]
            },
            "ban": {
                "function" : self.ban,
                "roles" : ["manager"]
            }
        }

    @classmethod
    def get_connection(cls):
        """Gets a connection to the database"""
        return pymysql.connect(
            host=tokens.MYSQL.HOST,
            user=tokens.MYSQL.USER,
            password=tokens.MYSQL.PASS,
            db=tokens.MYSQL.DATA,
            cursorclass=pymysql.cursors.DictCursor
        )

    def insert(self, event_type, member, content):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `bot_events` (`type`, `id`, `content`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (event_type, str(member.id), content ))
                connection.commit()
        finally:
            connection.close()

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
                    self.insert("froze", user, "{0.display_name} ({0.id}) was frozen by {1.display_name} ({1.id})".format(user, message.author))
            else:
                await message.channel.send("Can't find that user.")

    async def unfreeze(self, args, message):
        """Unfreeze a user from sending messages"""
        parser = argparse.ArgumentParser(description=self.unfreeze.__doc__)
        parser.add_argument("user", help="The user to unfreeze")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            user = message.channel.guild.get_member(self.bot.get_from_tag(args.user))
            if user != None:
                await user.remove_roles(self.getRole(message.channel.guild,"Silenced"))
                await message.channel.send("Unfroze {0.display_name}".format(user))
                self.insert("unfroze", user, "{0.display_name} ({0.id}) was unfrozen by {1.display_name} ({1.id})".format(user, message.author))
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
                            description += "    "+c['function'].__doc__+"\n"
                        await message.channel.send(
                            embed=embed,
                            content="```\n"+description+"```"
                        )
                    else:
                        await message.channel.send(embed=embed)
                else:
                    await message.channel.send("That extension does not exist.")

    async def speak(self, args, message):
        """Makes the bot say something"""
        parser = argparse.ArgumentParser(description=self.speak.__doc__)
        parser.add_argument("channel", help="The channel")
        parser.add_argument("words", nargs="+", type=str)
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            channel = discord.utils.find(lambda c: c.name == args.channel, message.channel.guild.channels)
            if channel is not None:
                await channel.send(" ".join(args.words))
                self.insert("bot-speak", message.author, "{0.display_name} ({0.id}) used the bot to post in {1.name} ({1.id}): {2}".format(message.author, channel, " ".join(args.words)))

    async def anon(self, args, message):
        """Send a message to the Manager anonymously"""
        if not isinstance(message.channel, discord.DMChannel):
            await message.delete()
            await message.channel.send("Only use this command in a direct message.")
        else:
            channel = discord.utils.find(lambda c: c.name == "inbox", discord.utils.find(lambda g: g.name == "Synixe", self.bot.guilds).channels)
            if channel is not None:
                await channel.send(" ".join(args))
                await message.channel.send("Message sent!")

    async def runas(self, args, message):
        """Run a command as a different member"""
        parser = argparse.ArgumentParser(description=self.runas.__doc__)
        parser.add_argument("member", help="User to run the command as")
        parser.add_argument("command", nargs="+", type=str)
        args = await self.bot.parse_args(parser, args, message)
        if isinstance(message.channel, discord.DMChannel):
            await message.channel.send("You can not use `runas` in a DM")
            return
        if args != False:
            user = message.channel.guild.get_member(self.bot.get_from_tag(args.member))
            if user != None:
                if args.command[0].startswith(self.bot.prefix):
                    args.command[0] = args.command[0][len(self.bot.prefix):]
                if args.command[0] in self.bot.commands:
                    cmd = args.command[0]
                    if self.bot.in_role_list(message.author, self.bot.commands[cmd]["roles"]) or "@everyone" in self.bot.commands[cmd]["roles"]:
                        message.author = user
                        args.command[0] = self.bot.prefix + args.command[0]
                        message.content = " ".join(args.command)
                        await message.channel.send("Executing `{}` as {}".format(message.content, user.display_name))
                        await self.bot.execute(message)
                    else:
                        await message.channel.send("You are not allowed to run commands with elevated privileges.")
                else:
                    await message.channel.send("That command does not exist!")
            else:
                await message.channel.send("That member was not found.")

    async def kick(self, args, message):
        """Kick a user"""
        parser = argparse.ArgumentParser(description=self.kick.__doc__)
        parser.add_argument("member", help="User to kick")
        parser.add_argument("reason", nargs="+", type=str)
        args = await self.bot.parse_args(parser, args, message)
        args.reason = " ".join(args.reason)
        if isinstance(message.channel, discord.DMChannel):
            await message.channel.send("This is a DM, nobody here to kick.")
            return
        if args != False:
            user = message.channel.guild.get_member(self.bot.get_from_tag(args.member))
            if user != None:
                channel = discord.utils.find(lambda c: c.name == "botevents", message.guild.channels)
                if channel != None:
                    text = "{0.display_name} ({0.id}) was kicked by {1.display_name} ({1.display_name})\nReason: {2}".format(user.display_name, message.author.display_name, args.reason)
                    await channel.send(text)
                    self.insert('kicked', user, text)
                await message.guild.kick(user=user, reason=args.reason)

    async def ban(self, args, message):
        """Ban a user"""
        parser = argparse.ArgumentParser(description=self.kick.__doc__)
        parser.add_argument("member", help="User to kick")
        parser.add_argument("reason", nargs="+", type=str)
        args = await self.bot.parse_args(parser, args, message)
        args.reason = " ".join(args.reason)
        if isinstance(message.channel, discord.DMChannel):
            await message.channel.send("This is a DM, nobody here to ban.")
            return
        if args != False:
            user = message.channel.guild.get_member(self.bot.get_from_tag(args.member))
            if user != None:
                channel = discord.utils.find(lambda c: c.name == "botevents", message.guild.channels)
                if channel != None:
                    text = "{0.display_name} ({0.id}) was banned by {1.display_name} ({1.display_name})\nReason: {2}".format(user.display_name, message.author.display_name, args.reason)
                    await channel.send(text)
                    self.insert('banned', user, text)
                await message.guild.ban(user=user, reason=args.reason)


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
