import discord
import argparse
import random

class BotExtension:
    def __init__(self, bot):
        self.bot = bot
        self.name = "Games"
        self.author = "nameless"
        self.version = "1.0.3"

    def register (self):
        return {
            "rps" : {
                "function": self.rps,
                "description": "Play Rock Paper Scissors against the bot",
                "roles" : ["@everyone"]
            }
        }

    async def rps(self, args, message):
        valid = ["paper", "rock", "scissors"]
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Play Rock Paper Scissors", message))
        parser.add_argument("choice",help=self.bot.processOutput("Your choice", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            if not args.choice.lower() in valid:
                await message.channel.send("That is not a valid choice")
                return
            hand = random.randint(0,2)
            if hand == 0:
                output = "Rock"
            if hand == 1:
                output = "Paper"
            if hand == 2:
                output = "Scissors"
            await message.channel.send(output)
