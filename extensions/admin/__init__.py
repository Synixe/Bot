import argparse
import random
import logger
import discord

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
                "description" : "Clears the past n number of messages (Default: 100)",
                "roles" : ["manager"]
            },
            "ext" : {
                "function" : self.ext,
                "description" : "Get info about loaded extensions",
                "roles" : ["moderator"]
            }
        }

    async def clear(self, args, message):
        parser = argparse.ArgumentParser(description="Clears the past *n* number of messages")
        parser.add_argument("n", nargs="?", default=20, type=int, help="The number of messages to delete, default: 20")
        parser.add_argument("--pinned",action="store_true",help="Delete pinned messages")
        args = parser.parse_args(args)
        messages = message.channel.history(limit=args.n + 2)
        status = await message.channel.send("Clearing {0} messages".format(args.n + 2))
        x = args.n + 2
        async for log in messages:
            if args.pinned or not log.pinned:
                try:
                    if log.id != status.id:
                        await log.delete()
                except:
                    logger.error("Failed to delete a message during Clear.")
            x -= 1
            await status.edit(content="Clearing {0} messages".format(x))
        await status.delete()


    async def ext(self, args, message):
        parser = argparse.ArgumentParser(description="Get info about loaded extensions")
        parser.add_argument("extension", nargs="?", type=str, help="The extension to get info about")
        args = parser.parse_args(args)
        if args.extension == None:
            embed = discord.Embed(
                title = self.bot.user.display_name,
                description = ", ".join(self.bot.extension_list)
            )
            embed.add_field(name="Commands",value=self.bot._num_commands)
            embed.add_field(name="Handlers",value=self.bot._num_handlers)
            embed.add_field(name="Loops", value=self.bot._num_loops)
            await message.channel.send(embed=embed)
        else:
            if args.extension in self.bot.extension_list:
                embed = discord.Embed(
                    title = self.bot.extensions[args.extension].name
                )
                if args.extension in self.bot._ext_commands:
                    embed.add_field(name="Commands",value=", ".join(self.bot._ext_commands[args.extension]))
                if args.extension in self.bot._ext_handlers:
                    embed.add_field(name="Handlers",value=", ".join(self.bot._ext_handlers[args.extension]))
                if args.extension in self.bot._ext_loops:
                    embed.add_field(name="Loops", value=", ".join(self.bot._ext_loops[args.extension]))
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("That extension does not exist.")

    async def on_message(self, message):
        if message.author.id == 307524009854107648:
            if random.random() < 0.05:
                await message.channel.send("Allegedly...")
        elif message.author.id == 206663073769979904:
            if random.random() < 0.05:
                await message.channel.send("Whatever you say nameless...")
