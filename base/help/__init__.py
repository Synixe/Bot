import bot

class Help(bot.Extension):
    """Provides helpful information regarding the bot's use"""

    @bot.role("manager")
    @bot.command()
    async def test(ctx, message):
        """Displays test info"""
        await message.channel.send("Hello")
