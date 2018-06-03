import discord
import logger
import bot
import extensions

import re
import io
from contextlib import redirect_stdout

class Client(discord.Client):
    async def on_connect(self):
        logger.debug("Connected to Discord")

    async def on_ready(self):
        logger.info("Connected as {0.name} ({0.id})".format(self.user), "green")
        self.extensions = []
        logger.info("Loading Base Extensions")
        self.base_extensions = extensions.get('base')
        logger.info("Loading Extensions")
        self.extensions = extensions.get('extensions') + self.base_extensions
        logger.info("Ready", "green")

    async def execute(self, message, profile=False):
        if message.author.id == self.user.id:
            return
        if message.content.startswith(self.profile.prefix):
            raw = message.content[len(self.profile.prefix):].split()
        else:
            raw = message.content.split(" ", 2)[1:]
        cmd = raw[0].lower()
        args = " ".join(raw[1:])
        args = re.compile(r'''((?:[^\s"']|"[^"]*"|'[^']*')+)''').split(args)[1::2]
        new = []
        for arg in args:
            new.append(arg.strip("\""))
        args = new
        for ext in self.extensions:
            for c in ext.commands:
                if c.name == cmd:
                    if bot.in_role_list(message.author, c.roles):
                        if profile:
                            import pprofile
                            profiler = pprofile.Profile()
                            with profiler():
                                await c.run(bot.Context(self, ext, message), args)
                            out = io.StringIO()
                            with redirect_stdout(out):
                                profiler.print_stats()
                            resp = out.getvalue().split("\n")
                            await bot.send_stats(c, self.profile.prefix, resp, raw, message.channel)
                        else:
                            await c.run(bot.Context(self, ext, message), args)
                    else:
                        await message.channel.send("You are not allowed to run that command.")

    async def on_message(self, message):
        await self.wait_until_ready()
        if message.author.id == self.user.id:
            return
        if (message.content.startswith(self.profile.prefix) and message.content.replace(self.profile.prefix, "").strip() != "") or (message.content.startswith(self.user.mention)):
            await self.execute(message)
        elif message.content.startswith("profile{}".format(self.profile.prefix)):
            message.content = message.content[7:]
            await self.execute(message, profile = True)
        else:
            await self.fire_event(message, "on_message")

    async def on_message_delete(self, message):
        await self.fire_event(message, "on_message_delete")

    async def on_message_edit(self, before, after):
        await self.fire_event([before, after], "on_message_edit")

    async def on_reaction_add(self, reaction, user):
        await self.fire_event([reaction, user], "on_reaction_add")

    async def on_reaction_remove(self, reaction, user):
        await self.fire_event([reaction, user], "on_reaction_remove")

    async def on_reaction_clear(self, message, reactions):
        await self.fire_event([message, reactions], "on_reaction_clear")

    async def on_member_join(self, member):
        await self.fire_event(member, "on_member_join")

    async def on_member_remove(self, member):
        await self.fire_event(member, "on_member_remove")

    async def on_member_update(self, before, after):
        await self.fire_event([before, after], "on_member_update")

    async def fire_event(self, args, event):
        await self.wait_until_ready()
        for ext in self.extensions:
            for h in ext.handlers:
                if h.event == event:
                    try:
                        await h.run(bot.Context(self, ext, args))
                    except Exception as e:
                        print("Error in "+event, str(e))
