import discord
import logger
import sys
import importlib
import os
import io
import random
from textblob import TextBlob
from contextlib import redirect_stdout, redirect_stderr

sys.path.insert(0, './extensions/')

class BotClient(discord.Client):
    supported_languages = ["af","sq","ar","az","eu","bn","be","bg","ca","zh-CN","zh-TW","hr","cs","da","nl","en","eo","et","tl","fi","fr","gl","ka","de","el","gu","ht","iw","hi","hu","is","id","ga","it","ja","kn","ko","la","lv","lt","mk","ms","mt","no","fa","pl","pt","ro","ru","sr","sk","sl","es","sw","sv","ta","te","th","tr","uk","vi","vy","yi"]
    async def on_ready(self):
        print("Connected")
        self.extension_list = [x[0].split('/')[1] for x in os.walk('extensions') if x[0].count('/') == 1]
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
        logger.info("Connected as {0.name} ({0.id})".format(self.user))
        for exten in self.extension_list:
            loaded = importlib.import_module(exten).BotExtension(self)
            self.extensions[exten] = loaded
            if hasattr(loaded,"active"):
                if not loaded.active:
                    continue
            logger.info("Loading {0.name} {0.version} by {0.author}".format(loaded))
            if hasattr(loaded, "register"):
                newcmds = loaded.register()
                self.commands.update(newcmds)
                self._ext_commands[exten] = newcmds
                self._num_commands += len(newcmds)
                for c in newcmds:
                    logger.info("\tCommand Registered: {0}".format(c))
            if hasattr(loaded, "loops"):
                newloops = loaded.loops()
                self.loops.update(newloops)
                self._ext_loops[exten] = newloops
                self._num_loops += len(newloops)
                for l in newloops:
                    logger.info("\tLoop Registered: {0}".format(l))
            for h in ["on_message","on_member_join","on_member_remove","on_member_update","on_member_ban","on_member_unban"]:
                if h not in self.handlers:
                    self.handlers[h] = []
                if hasattr(loaded, h):
                    if exten not in self._ext_handlers:
                        self._ext_handlers[exten] = []
                    logger.info("\tHandler Registered: {0}".format(h))
                    self._num_handlers += 1
                    self.handlers[h].append(loaded)
                    self._ext_handlers[exten].append(h)
        logger.info("Initialized")
        logger.info("Commands: {0}".format(self._num_commands))
        logger.info("Handlers: {0}".format(self._num_handlers))
        logger.info("Loops: {0}".format(self._num_loops))
        print("Ready!")

    async def execute(self, message):
        if message.author.id == self.user.id:
            return #Do not allow responding to it's own commands
        raw = message.content[len(self.prefix):].split()
        cmd = raw[0]
        args = " ".join(raw[1:])
        import re
        args = re.compile(r'''((?:[^\s"']|"[^"]*"|'[^']*')+)''').split(args)[1::2]
        if cmd in self.commands:
            if self.inRoleList(message.author, self.commands[cmd]["roles"]) or (isinstance(message.channel, discord.DMChannel) and "@everyone" in self.commands[cmd]["roles"]):
                o = io.StringIO()
                e = io.StringIO()
                with redirect_stdout(o):
                    with redirect_stderr(e):
                        try:
                            await self.commands[cmd]["function"](args, message)
                            out = e.getvalue()
                            if out != "":
                                logger.error(out)
                        except SystemExit:
                            if str(sys.exc_info()[1]) == '0':
                                out = o.getvalue()
                            else:
                                out = e.getvalue()
                            await message.channel.send(out.replace("main.py",self.prefix+cmd))

            else:
                if isinstance(message.channel, discord.DMChannel):
                    await message.channel.send(self.processOutput("This command can not be used in a direct message channel.", message))
                else:
                    await message.channel.send(self.processOutput("Sorry, you are not allowed to use that command.", message))
        else:
            await message.channel.send(self.processOutput("That command doesn't exist... You can use `?ext` to learn about what I can do", message))

    async def on_message(self, message):
        await self.wait_until_ready()
        if message.author.id != self.user.id:
            if message.content.startswith(self.prefix) and message.content.replace(self.prefix,"").strip() != "":
                await self.execute(message)
            else:
                for h in self.handlers["on_message"]:
                    await h.on_message(message)

    async def on_member_join(self, member):
        await self.wait_until_ready()
        for h in self.handlers["on_member_join"]:
            await h.on_member_join(member)

    async def on_member_remove(self, member):
        await self.wait_until_ready()
        for h in self.handlers["on_member_remove"]:
            await h.on_member_remove(member)

    async def on_member_ban(self, member):
        await self.wait_until_ready()
        for h in self.handlers["on_member_ban"]:
            await h.on_member_ban(member)

    async def on_member_unban(self, member):
        await self.wait_until_ready()
        for h in self.handlers["on_member_unban"]:
            await h.on_member_unban(member)

    async def on_member_update(self, before, after):
        await self.wait_until_ready()
        for h in self.handlers["on_member_update"]:
            await h.on_member_update(before, after)

    @classmethod
    def inRoleList(cls, member, roles):
        if "@everyone" in roles:
            return True
        if isinstance(member, discord.User):
            return False
        for r in member.roles:
            if r.name.lower() in roles:
                return True
        return False

    @classmethod
    def getIDFromTag(cls, text):
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

    def processOutput(self, response, message):
        if message.author.id == 206663073769979904:
            en_blob = TextBlob(response)
            return str(en_blob.translate(to=random.choice(self.supported_languages)))
        return response
