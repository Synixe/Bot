"""Games for Disco"""
import itertools
import collections
import random
import bot

class SimpleGames(bot.Extension):
    """Games for Disco"""

    @bot.command()
    async def flip(ctx, message):
        """Flip a coin"""
        side = random.randint(0, 1)
        if side == 0:
            output = "It lands on heads"
        else:
            output = "It lands on tails"
        await message.channel.send(output)

    @bot.argument("[sides+]", int, default=6)
    @bot.command()
    async def dice(ctx, message):
        """Roll a dice"""
        await message.channel.send(random.choice(
            ["The value is {0}", "You rolled a {0}", "It lands on {0}"]
        ).format(random.randint(1, ctx.args.sides)))

    @bot.argument("choice")
    @bot.command()
    async def rps(ctx, message):
        """Rock, Paper, Scissors Game"""
        valid = ["rock", "paper", "scissors"]
        if not ctx.args.choice.lower() in valid:
            await message.channel.send("That is not a valid choice")
            return
        bot = random.randint(0, 2)
        if bot == 0:
            output = "Rock"
        if bot == 1:
            output = "Paper"
        if bot == 2:
            output = "Scissors"
        player = valid.index(ctx.args.choice.lower())
        if player == bot:
            output += ", it's a tie."

        elif player == bot - 1 or player == bot + 2:
            output += ", you lose."
        elif player == bot + 1 or player == bot - 2:
            output += ", you win."
        await message.channel.send(output)

    @bot.argument("question")
    @bot.command()
    async def ball(ctx, message):
        """8-Baller"""
        lines = {}
        for line in open("./extensions/games/8ball.txt").read().splitlines():
            value, text = line.split(":", 1)
            lines[text] = int(value)
        lines = collections.Counter(lines)
        i = random.randrange(sum(lines.values()))
        text = next(itertools.islice(lines.elements(), i, None))
        await message.channel.send(text)
