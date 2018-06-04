import bot
import logger

class DevTools(bot.Extension):
    """Provides information about the Bot and loaded extensions"""

    @bot.role("code contributer")
    @bot.dev()
    @bot.command()
    async def stop(ctx, message):
        """Shutdown the bot"""
        await message.channel.send("Stopping Bot")
        logger.info("Bot shutdown by {0.display_name} ({0.id})".format(message.author))
        await ctx._bot.logout()

    @bot.role("code contributer")
    @bot.dev()
    @bot.command()
    async def ping(ctx, message):
        """Displays the ping to Discord"""
        await message.channel.send("{:0.0f}ms".format(ctx._bot.latency * 1000))
