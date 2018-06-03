import bot
import logger

import json
import sys

class DevTools(bot.Extension):
    """Provides information about the Bot and loaded extensions"""

    @bot.role("code contributer")
    @bot.dev()
    @bot.command()
    async def stop(ctx, message):
        """Displays a copy of the current context"""
        await message.channel.send("Stopping Bot")
        logger.info("Bot shutdown by {0.display_name} ({0.id})".format(message.author))
        await ctx._bot.logout()
