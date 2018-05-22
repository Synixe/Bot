"""Creating Polls for Disco"""
import discord
import bot

class Polls(bot.Extension):
    """Polls for Disco"""

    @bot.role("active")
    @bot.role("new")
    @bot.role("inactive")
    @bot.argument("text+")
    @bot.command()
    async def poll(ctx, message):
        """Birth of Polls"""
        msg = await message.channel.send(ctx.args.text)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
