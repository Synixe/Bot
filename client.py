"""Bot Core Component"""
import sys
import logger
try:
    import discord
    if discord.__version__.startswith("0"):
        logger.error("You need to be using a newer version of discord.py.")
        logger.error("Run setup.py to update")
        sys.exit(1)
except ImportError:
    logger.error("You are missing discord.py.")
    logger.error("Run setup.py to install it")
import importlib
import os
import io
import socket
import traceback
import asyncio
import re
from sys import platform
from contextlib import redirect_stdout, redirect_stderr

sys.path.insert(0, './extensions/')

class BotClient(discord.Client):
    """Bot Core Component"""
    async def on_ready(self):
        """Load the extensions for the bot"""
        if self.user.id == 403101852771680258:
            self.prefix = "?"
        elif socket.gethostname() in ["yehuda", "DESKTOP-5CJEEUH"]:
            self.prefix = "."
        else:
            self.prefix = ">"
        if platform == "linux" or platform == "linux2":
            self.extension_list = [x[0].split('/')[1] for x in os.walk('extensions') if x[0].count('/') == 1]
        else:
            self.extension_list = [x[0][13:] for x in os.walk('./extensions') if x[0].count('/') == 1 and "__pycache__" not in x[0]][1:]
        self.extensions = {}
        self.commands = {}
        self._ext_commands = {}
        self.handlers = {}
        self._ext_handlers = {}
        self.loops = {}
        self._ext_loops = {}
        self._num_commands = 0
        self._num_handlers = 0
        self._num_loops = 0
        logger.info("Connected as {0.name} ({0.id})".format(self.user), "green")
        logger.debug("Loading Extensions")
        for exten in self.extension_list:
            loaded = importlib.import_module(exten).BotExtension(self)
            self.extensions[exten] = loaded
            if hasattr(loaded, "active"):
                if not loaded.active:
                    continue
            disable = False
            if self.user.id != 403101852771680258:
                if hasattr(loaded, "disable_during_test"):
                    disable = loaded.disable_during_test
                    logger.debug("Ignoring {0.name} {0.version} by {0.author}".format(loaded), "red")
            if not disable:
                logger.debug("{0.name} {0.version} by {0.author}".format(loaded))
            if hasattr(loaded, "__register__"):
                newcmds = loaded.__register__()
                if not disable:
                    self.commands.update(newcmds)
                    self._ext_commands[exten] = newcmds
                    self._num_commands += len(newcmds)
                    for command in newcmds:
                        logger.debug("\tCommand: {0}".format(command))
                        if "alias" in newcmds[command]:
                            for alias in newcmds[command]["alias"]:
                                logger.debug("\t\tAlias: {}".format(alias))
                                alias_f = {alias : {
                                    "function": newcmds[command]["function"],
                                    "roles": newcmds[command]["roles"]
                                }}
                                self.commands.update(alias_f)
                else:
                    for command in newcmds:
                        logger.debug("\tCommand Ignored: {0}".format(command), "red")
                        self.commands[command] = {"function": self.disabled, "roles": ["@everyone"]}
            if hasattr(loaded, "__loops__"):
                if not disable:
                    newloops = loaded.__loops__()
                    self.loops.update(newloops)
                    self._ext_loops[exten] = newloops
                    self._num_loops += len(newloops)
                    for loop in newloops:
                        logger.debug("\tLoop: {0}".format(loop))
            for handler in ["on_message", "on_member_join", "on_member_remove", "on_member_update", "on_member_ban", "on_member_unban", "on_reaction_add"]:
                if handler not in self.handlers:
                    self.handlers[handler] = []
                if hasattr(loaded, handler):
                    if exten not in self._ext_handlers:
                        self._ext_handlers[exten] = []
                    if not disable:
                        logger.debug("\tHandler: {0}".format(handler))
                        self._num_handlers += 1
                        self.handlers[handler].append(loaded)
                        self._ext_handlers[exten].append(handler)
                    else:
                        logger.debug("\tHandler: {0}".format(handler), "red")
        logger.info("✔️ {} Extensions Loaded".format(len(self.extension_list)))
        logger.debug("Commands: {}".format(self._num_commands))
        logger.debug("Handlers: {}".format(self._num_handlers))
        logger.debug("Loops: {}".format(self._num_loops))
        logger.info("Prefix: {}".format(self.prefix))
        logger.info("Bot Ready! ✔️", "green")

        self.loop.create_task(self.loop_monitor())

    async def loop_monitor(self):
        alerted = []
        guild = discord.utils.find(
            lambda g: g.name == "Synixe",
            self.guilds
        )
        while not self.is_closed():
            for l in self.loops:
                task = self.loops[l]
                if l not in alerted and task.done():
                    if task.exception() != None:
                        alerted.append(l)
                        exception = task.exception()
                        if str(exception) == "[Errno None] Cannot connect to host discordapp.com:443 ssl:True [Can not connect to discordapp.com:443 [None]]":
                            continue
                        message = "`{0}` occured in task `{1}`".format(
                            exception, l
                        )
                        stack = task.get_stack()
                        for frame in stack:
                            message += "\n`{0.f_code.co_filename}: {0.f_lineno}`".format(frame)

                        if self.user.id == 403101852771680258:
                            channel = discord.utils.find(lambda c: c.name == "errors", guild.channels)
                        else:
                            channel = discord.utils.find(lambda c: c.name == "bot", guild.channels)
                        await channel.send(message)
                        logger.error(message)
            await asyncio.sleep(10)

    async def execute(self, message):
        """Execute a command"""
        if message.author.id == self.user.id:
            return #Do not allow responding to it's own commands
        raw = message.content[len(self.prefix):].split()
        cmd = raw[0].lower()
        args = " ".join(raw[1:])
        args = re.compile(r'''((?:[^\s"']|"[^"]*"|'[^']*')+)''').split(args)[1::2]
        new = []
        for arg in args:
            new.append(arg.strip("\""))
        args = new
        if cmd in self.commands:
            if self.in_role_list(message.author, self.commands[cmd]["roles"]) or (isinstance(message.channel, discord.DMChannel) and "@everyone" in self.commands[cmd]["roles"]):
                try:
                    await self.commands[cmd]["function"](args, message)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    tb = traceback.format_exc()
                    if self.user.id == 403101852771680258:
                        await message.channel.send("Oh no! :cry: An error occurred. It has been reported to the Code Contributers.")
                        channel = discord.utils.find(lambda c: c.name == "errors", message.guild.channels)
                    else:
                        channel = message.channel
                    await channel.send(
                        "An error occured during the execution of `{}` by {} in {}\n\n```py\n{}\n```"
                        .format(message.content, message.author.display_name, message.channel.mention, tb)
                    )
                    logger.error("An error occured: "+str(tb))
            else:
                if isinstance(message.channel, discord.DMChannel):
                    await message.channel.send("This command can not be used in a direct message channel.")
                else:
                    await message.channel.send("Sorry, you are not allowed to use that command.")
        else:
            await message.channel.send("That command doesn't exist... You can use `{}help` to learn about what I can do".format(self.prefix))

    async def on_message(self, message):
        """Execute commands, if the message is not a command pass it on to extensions"""
        await self.wait_until_ready()
        if message.author.id != self.user.id:
            if message.content.startswith(self.prefix) and message.content.replace(self.prefix,"").strip() != "":
                await self.execute(message)
            else:
                for handler in self.handlers["on_message"]:
                    await handler.on_message(message)

    async def on_member_join(self, member):
        """Call on_member_join inside extensions"""
        await self.wait_until_ready()
        for handler in self.handlers["on_member_join"]:
            await handler.on_member_join(member)

    async def on_member_remove(self, member):
        """Call on_member_remove inside extensions"""
        await self.wait_until_ready()
        for handler in self.handlers["on_member_remove"]:
            await handler.on_member_remove(member)

    async def on_member_ban(self, member):
        """Call on_member_ban inside extensions"""
        await self.wait_until_ready()
        for handler in self.handlers["on_member_ban"]:
            await handler.on_member_ban(member)

    async def on_member_unban(self, member):
        """Call on_member_unban inside extensions"""
        await self.wait_until_ready()
        for handler in self.handlers["on_member_unban"]:
            await handler.on_member_unban(member)

    async def on_member_update(self, before, after):
        """Call on_member_update inside extensions"""
        await self.wait_until_ready()
        for handler in self.handlers["on_member_update"]:
            await handler.on_member_update(before, after)

    async def on_reaction_add(self, reaction, member):
        """Call on_reaction_add inside extensions"""
        await self.wait_until_ready()
        for handler in self.handlers["on_reaction_add"]:
            await handler.on_reaction_add(reaction, member)

    async def disabled(self, args, message):
        """This function is not allowed during testing"""
        await message.channel.send("That command is disabled during testing")

    @classmethod
    def in_role_list(cls, member, roles):
        """Check if a member is in a list of roles"""
        if "@everyone" in roles:
            return True
        if isinstance(member, discord.User):
            return False
        for role in member.roles:
            if role.name.lower() in roles:
                return True
        return False

    @classmethod
    def get_from_tag(cls, text):
        """Get a user or channel's id from a mention"""
        if text.startswith("<@") or text.startswith("<#"):
            try:
                return int(text[2:-1])
            except ValueError:
                return int(text[3:-1])
        else:
            try:
                return int(text)
            except ValueError:
                return text

    async def parse_args(self, parser, args, message):
        """Parse args and display errors"""
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out):
            with redirect_stderr(err):
                try:
                    return parser.parse_args(args)
                except SystemExit:
                    if str(sys.exc_info()[1]) == '0':
                        resp = out.getvalue()
                    else:
                        resp = err.getvalue()
                    await message.channel.send(resp.replace("main.py", self.prefix+message.content[len(self.prefix):].split()[0]))
        return False
