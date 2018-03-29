"""Games for Discord"""
import argparse
import random
import itertools
import collections
import discord
import logger

class BotExtension:
    """Games for Discord"""
    def __init__(self, bot):
        self.bot = bot
        self.name = "Games"
        self.author = "nameless"
        self.version = "1.3"

    def __register__(self):
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
            },
            "8ball" : {
                "function" : self.ball,
                "roles" : ["@everyone"],
                "alias" : ["🎱"]
            }
        }

    async def rps(self, args, message):
        """Play Rock Paper Scissors against the bot"""
        valid = ["rock", "paper", "scissors"]
        parser = argparse.ArgumentParser(description=self.rps.__doc__)
        parser.add_argument("choice", help="Your choice")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            if not args.choice.lower() in valid:
                await message.channel.send("That is not a valid choice")
                return
            bot = random.randint(0, 2)
            if bot == 0:
                output = "Rock"
            if bot == 1:
                output = "Paper"
            if bot == 2:
                output = "Scissors"
            player = valid.index(args.choice.lower())
            if player == bot:
                output += ", it's a tie."

            elif player == bot - 1 or player == bot + 2:
                output += ", you lose."
            elif player == bot + 1 or player == bot - 2:
                output += ", you win."
            await message.channel.send(output)

    async def dice(self, args, message):
        """Roll a dice"""
        parser = argparse.ArgumentParser(description=self.dice.__doc__)
        parser.add_argument("n", nargs="?", type=int, default=6, help="Number of sides")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            value = random.randint(1, args.n)
            messages = ["The value is {0}", "You rolled a {0}", "It lands on {0}"]
            await message.channel.send(random.choice(messages).format(value))

    async def flip(self, args, message):
        """Flip a coin"""
        parser = argparse.ArgumentParser(self.flip.__doc__)
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            side = random.randint(0, 1)
            if side == 0:
                output = "It lands on heads"
            else:
                output = "It lands on tails"
            await message.channel.send(output)

    async def ball(self, args, message):
        """8-Ball Magic"""
        parser = argparse.ArgumentParser(self.ball.__doc__)
        parser.add_argument("question", nargs="+", help="A question for the 8-Ball")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            lines = {}
            for line in open("./extensions/games/8ball.txt").read().splitlines():
                value, text = line.split(":", 1)
                lines[text] = int(value)
            lines = collections.Counter(lines)
            i = random.randrange(sum(lines.values()))
            text = next(itertools.islice(lines.elements(), i, None))
            await message.channel.send(text)
