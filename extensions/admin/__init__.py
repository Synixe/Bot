import argparse
import random
import logger
import discord
import gifs
import sys

class BotExtension:
    def __init__(self, bot):
        self.name = "Admin Tools"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def register(self):
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
                "roles" : ["manager","moderator"]
            },
            "unfreeze" : {
                "function" : self.unfreeze,
                "roles" : ["manager","moderator"]
            },
            "speak" : {
                "function" : self.speak,
                "roles" : ["manager"]
            },
            "anon" : {
                "function" : self.anon,
                "roles" : ["@everyone"]
            },
            "stop" : {
                "function" : self.stop,
                "roles" : ["code contributer"]
            }
        }

    async def clear(self, args, message):
        """Clears the past n number of messages (Default: 20)"""
        parser = argparse.ArgumentParser(description=self.clear.__doc__)
        parser.add_argument("n", nargs="?", default=20, type=int, help=self.bot.processOutput("The number of messages to delete, default: 20", message))
        parser.add_argument("--pinned",action="store_true",help=self.bot.processOutput("Delete pinned messages", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            messages = message.channel.history(limit=args.n + 2)
            status = await message.channel.send(self.bot.processOutput("Clearing {0} messages".format(args.n + 2), message))
            x = args.n + 2
            async for log in messages:
                if args.pinned or not log.pinned:
                    try:
                        if log.id != status.id:
                            await log.delete()
                    except discord.errors.NotFound:
                        logger.error("Failed to delete a message during clear.")
                x -= 1
                try:
                    await status.edit(content=self.bot.processOutput("Clearing {0} messages".format(x), message))
                except discord.errors.NotFound:
                    #Chances are 2 clear functions are running, stop this one
                    return
            await status.delete()

    async def freeze(self, args, message):
        """Freeze a user from sending messages"""
        parser = argparse.ArgumentParser(description=self.freeze.__doc__)
        parser.add_argument("user", help=self.bot.processOutput("The user to freeze", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            user = message.channel.guild.get_member(self.bot.getIDFromTag(args.user))
            if user != None:
                if self.bot.inRoleList(user, ["manager"]):
                    async with message.channel.typing():
                        await message.channel.send(file=discord.File(fp=gifs.getRandom("treason")))
                else:
                    await user.add_roles(self.getRole(message.channel.guild,"Silenced"))
                    await message.channel.send(self.bot.processOutput("Froze {0.display_name}".format(user), message))
            else:
                await message.channel.send(self.bot.processOutput("Can't find that user.", message))

    async def unfreeze(self, args, message):
        """"Unfreeze a user from sending messages"""
        parser = argparse.ArgumentParser(description=self.unfreeze.__doc__)
        parser.add_argument("user", help=self.bot.processOutput("The user to unfreeze", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            user = message.channel.guild.get_member(self.bot.getIDFromTag(args.user))
            if user != None:
                await user.remove_roles(self.getRole(message.channel.guild,"Silenced"))
                await message.channel.send(self.bot.processOutput("Unfroze {0.display_name}".format(user), message))
            else:
                await message.channel.send(self.bot.processOutput("Can't find that user.", message))

    async def ext(self, args, message):
        """Get info about loaded extensions"""
        parser = argparse.ArgumentParser(description=self.ext.__doct__)
        parser.add_argument("extension", nargs="?", type=str, help=self.bot.processOutput("The extension to get info about", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            if args.extension == None:
                embed = discord.Embed(
                    title = self.bot.user.display_name,
                    description = ", ".join(self.bot.extension_list)
                )
                embed.set_footer(text=self.bot.processOutput("Use ?ext [module] to see commands and handlers.", message))
                embed.add_field(name=self.bot.processOutput("Commands", message),value=self.bot._num_commands)
                embed.add_field(name=self.bot.processOutput("Handlers", message),value=self.bot._num_handlers)
                embed.add_field(name=self.bot.processOutput("Loops", message), value=self.bot._num_loops)
                await message.channel.send(embed=embed)
            else:
                if args.extension in self.bot.extension_list:
                    if hasattr(self.bot.extensions[args.extension],"active"):
                        if not self.bot.extensions[args.extension].active:
                            color = discord.Colour.from_rgb(r=255,g=0,b=0)
                        else:
                            color = discord.Colour.from_rgb(r=0,g=255,b=0)
                    else:
                        color = discord.Colour.from_rgb(r=0,g=255,b=0)
                    embed = discord.Embed(
                        title = "{0.name} v{0.version} by {0.author}".format(self.bot.extensions[args.extension]),
                        color = color
                    )
                    if args.extension in self.bot._ext_handlers:
                        embed.add_field(name=self.bot.processOutput("Handlers", message),value=", ".join(self.bot._ext_handlers[args.extension]))
                    if args.extension in self.bot._ext_loops:
                        embed.add_field(name=self.bot.processOutput("Loops", message), value=", ".join(self.bot._ext_loops[args.extension]))
                    if args.extension in self.bot._ext_commands:
                        description = ""
                        for name, c in self.bot._ext_commands[args.extension].items():
                            description += name+"\n"
                            description += "    "+c['description']+"\n"
                        await message.channel.send(embed=embed,content=self.bot.processOutput("```\n"+description+"```", message))
                    else:
                        await message.channel.send(embed=embed)
                else:
                    await message.channel.send(self.bot.processOutput("That extension does not exist.", message))

    async def speak(self, args, message):
        """"Makes the bot say something funny"""
        parser = argparse.ArgumentParser(description=self.speak.__doc__)
        parser.add_argument("channel", help=self.bot.processOutput("The channel", message))
        parser.add_argument("words",nargs="+",type=str)
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            channel = discord.utils.find(lambda c: c.name == args.channel, message.channel.guild.channels)
            if channel is not None:
                await channel.send(" ".join(args.words))
            else:
                frame = getframeinfo(currentframe())
                logger.throw("Unable to find #{0.name}\n\t{1.filename} line {0.lineno - 4}".format(args.channel, frame))

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

    async def stop(self, args, message):
        """Stop the bot"""
        sys.exit(0)

    @classmethod
    def getRole(cls, guild, name):
        for r in guild.roles:
            if name.lower() == r.name.lower():
                return r
        return None

    async def on_message(self, message):
        if message.author.id == 307524009854107648:
            if random.random() < 0.01:
                await message.channel.send("Allegedly...")
