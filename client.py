import discord
import logger
import sys
import importlib
import os
import traceback
import io
from contextlib import redirect_stdout, redirect_stderr

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

sys.path.insert(0, './extensions/')

extension_list = [x[0].split('/')[1] for x in os.walk('extensions') if x[0].count('/') == 1]

class BotClient(discord.Client):
    async def on_ready(self):
        self.extensions = []
        self.commands = {}
        self.handlers = {}
        self._num_commands = 0
        self._num_handlers = 0
        logger.info("Connected as {0.name} ({0.id})".format(self.user))
        for exten in extension_list:
            loaded = importlib.import_module(exten).BotExtension(self)
            self.extensions.append(loaded)
            logger.info("Loading {0.name} {0.version} by {0.author}".format(loaded))
            if hasattr(loaded, "register"):
                newcmds = loaded.register()
                self.commands.update(newcmds)
                self._num_commands += len(newcmds)
                for c in newcmds:
                    logger.info("\tCommand Registered: {0}".format(c))
            for h in ["on_message","on_member_join","on_member_remove","on_member_update"]:
                if h not in self.handlers:
                    self.handlers[h] = []
                if hasattr(loaded, h):
                    logger.info("\tHandler Registered: {0}".format(h))
                    self._num_handlers += 1
                    self.handlers[h].append(loaded)
        logger.info("Initialized")
        logger.info("Commands: {0}".format(self._num_commands))
        logger.info("Handlers: {0}".format(self._num_handlers))
        print("Ready!")

    async def execute(self, message):
        if message.author.id == self.user.id:
            return #Do not allow responding to it's own commands
        raw = message.content[len(self.prefix):].split()
        cmd = raw[0]
        args = raw[1:]
        if cmd in self.commands:
            if self.inRoleList(message.author, self.commands[cmd]["roles"]):
                o = io.StringIO()
                e = io.StringIO()
                with redirect_stdout(o):
                    with redirect_stderr(e):
                        try:
                            await self.commands[cmd]["function"](args, message)
                        except SystemExit:
                            if str(sys.exc_info()[1]) == '0':
                                out = o.getvalue()
                            else:
                                out = e.getvalue()
                            await message.channel.send(out.replace("main.py",self.prefix+cmd))
            else:
                await message.channel.send("Sorry, you are not allowed to use that command.")
        else:
            await message.channel.send("That command doesn't exist...")

    async def on_message(self, message):
        if message.content.startswith(self.prefix):
            await self.execute(message)
        else:
            for h in self.handlers["on_message"]:
                await h.on_message(message)

    async def on_member_join(self, member):
        for h in self.handlers["on_member_join"]:
            await h.on_member_join(member)

    async def on_member_remove(self, member):
        for h in self.handlers["on_member_remove"]:
            await h.on_member_remove(member)

    async def on_member_update(self, before, after):
        for h in self.handlers["on_member_update"]:
            await h.on_member_update(before, after)

    def inRoleList(self, member, roles):
        for r in member.roles:
            if r.name.lower() in roles:
                return True
        return False

    def getIDFromTag(self, text):
        if text.startswith("<@") or text.startswith("<#"):
            return int(text[2:-1])
        else:
            try:
                return int(text)
            except:
                return text
