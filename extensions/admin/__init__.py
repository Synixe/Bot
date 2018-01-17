import argparse
import random

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
            }
        }

    async def clear(self, args, message):
        parser = argparse.ArgumentParser(description="Clears the past *n* number of messages")
        parser.add_argument("n", nargs="?", default=20, type=int, help="The number of messages to delete, default: 20")
        parser.add_argument("--pinned",action="store_true",help="Delete pinned messages")
        args = parser.parse_args(args)
        async for log in message.channel.history(limit=args.n + 1):
            if args.pinned or not log.pinned:
                await log.delete()

    async def on_message(self, message):
        if message.author.id == 307524009854107648:
            if random.random() < 0.05:
                await message.channel.send("Allegedly...")
        elif message.author.id == 206663073769979904:
            if random.random() < 0.05:
                await message.channel.send("Whatever you say nameless...")
