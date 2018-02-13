"""Games for Discord"""
import argparse
import random
import discord


class BotExtension:
    """Adds games to the bot"""
    def __init__(self, bot):
        """Init with the bot object"""
        self.bot = bot
        self.name = "Games"
        self.author = "nameless"
        self.version = "1.1"

    def register(self):
        """Register with the main bot"""
        return {
            "rps" : {
                "function": self.rps,
                "roles" : ["@everyone"]
            },
            "dice" : {
                "function" : self.dice,
                "roles" : ["@everyone"]
            },
            "flip" : {
                "function" : self.flip,
                "roles" : ["@everyone"]
            }
        }

    async def rps(self, args, message):
        """Play Rock Paper Scissors against the bot"""
        valid = ["paper", "rock", "scissors"]
        parser = argparse.ArgumentParser(description=self.rps.__doc__)
        parser.add_argument("choice", help=self.bot.processOutput("Your choice", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            if not args.choice.lower() in valid:
                await message.channel.send("That is not a valid choice")
                return
            hand = random.randint(0, 2)
            if hand == 0:
                output = "Rock"
            if hand == 1:
                output = "Paper"
            if hand == 2:
                output = "Scissors"
            await message.channel.send(output)

    async def dice(self, args, message):
        """Roll a dice"""
        parser = argparse.ArgumentParser(description=self.dice.__doc__)
        parser.add_argument("n", nargs="?", type=int, default=6, help=self.bot.processOutput("Number of sides", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            value = random.randint(1, args.n)
            messages = ["The value is {0}", "You rolled a {0}", "It lands on {0}"]
            await message.channel.send(self.bot.processOutput(random.choice(messages).format(value),message))

    async def flip(self, args, message):
        """Flip a coin"""
        parser = argparse.ArgumentParser(self.flip.__doc__)
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            side = random.randint(0, 1)
            if side == 0:
                output = "It lands on heads"
            else:
                output = "It lands on tails"
            await message.channel.send(self.bot.processOutput(output, message))
