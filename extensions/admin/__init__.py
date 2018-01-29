import argparse
import random
import logger
import discord
import gifs

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
                "description" : "Clears the past n number of messages (Default: 20)",
                "roles" : ["manager"]
            },
            "ext" : {
                "function" : self.ext,
                "description" : "Get info about loaded extensions",
                "roles" : ["@everyone"]
            },
            "freeze" : {
                "function" : self.freeze,
                "description" : "Freeze a user from sending messages",
                "roles" : ["manager","moderator"]
            },
            "unfreeze" : {
                "function" : self.unfreeze,
                "description" : "Unfreeze a user from sending messages",
                "roles" : ["manager","moderator"]
            },
            "speak" : {
                "function" : self.speak,
                "description" : "Makes the bot say something funny",
                "roles" : ["manager"]
            }
        }

    async def clear(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Clears the past *n* number of messages", message))
        parser.add_argument("n", nargs="?", default=20, type=int, help=self.bot.processOutput("The number of messages to delete, default: 20", message))
        parser.add_argument("--pinned",action="store_true",help=self.bot.processOutput("Delete pinned messages", message))
        args = parser.parse_args(args)
        messages = message.channel.history(limit=args.n + 2)
        status = await message.channel.send(self.bot.processOutput("Clearing {0} messages".format(args.n + 2), message))
        x = args.n + 2
        async for log in messages:
            if args.pinned or not log.pinned:
                try:
                    if log.id != status.id:
                        await log.delete()
                except: #TODO specify error
                    logger.error(self.bot.processOutput("Failed to delete a message during Clear.", message))
            x -= 1
            await status.edit(content=self.bot.processOutput("Clearing {0} messages".format(x), message))
        await status.delete()

    async def freeze(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Freeze a user from sending messages", message))
        parser.add_argument("user", help=self.bot.processOutput("The user to freeze", message))
        args = parser.parse_args(args)
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
        parser = argparse.ArgumentParser(description=self.bot.processOutput("UnFreeze a user, allowing them to send messages", message))
        parser.add_argument("user", help=self.bot.processOutput("The user to unfreeze", messages))
        args = parser.parse_args(args)
        user = message.channel.guild.get_member(self.bot.getIDFromTag(args.user))
        if user != None:
            await user.remove_roles(self.getRole(message.channel.guild,"Silenced"))
            await message.channel.send(self.bot.processOutput("Unfroze {0.display_name}".format(user), messages))
        else:
            await message.channel.send(self.bot.processOutput("Can't find that user.", messages))

    async def ext(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Get info about loaded extensions", message))
        parser.add_argument("extension", nargs="?", type=str, help=self.bot.processOutput("The extension to get info about", message))
        args = parser.parse_args(args)
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
                    title = "{0.name} v{0.version}".format(self.bot.extensions[args.extension]),
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
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Make the bot speak", message))
        parser.add_argument("channel", help=self.bot.processOutput("The channel", message))
        parser.add_argument("words",nargs="+",type=str)
        args = parser.parse_args(args)
        channel = discord.utils.find(lambda c: c.name == args.channel, message.channel.guild.channels)
        if channel is not None:
            await channel.send(" ".join(args.words))
        else:
            frame = getframeinfo(currentframe())
            logger.throw("Unable to find #{0.name}\n\t{1.filename} line {0.lineno - 4}".format(args.channel, frame))

    @classmethod
    def getRole(cls, guild, name):
        for r in guild.roles:
            if name.lower() == r.name.lower():
                return r
        return None

    #async def on_message(self, message):
    #    if message.author.id == 307524009854107648:
    #        if random.random() < 0.02:
    #            await message.channel.send("Allegedly...")
