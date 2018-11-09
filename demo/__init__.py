import discord
import bot

class Demo(bot.Extension):
    """Demo Command"""
    @bot.command()
    async def demo(ctx, message):
        """A Simple Demo Command"""
        await message.add_reaction("🎉")
