import bot
import random

class SimpleGames(bot.Extension):

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
