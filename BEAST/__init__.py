"""🐕 BEAST for Disco"""
import bot
import discord

class BEAST(bot.Extension):
    """🐕"""

    @bot.event("on_message")
    async def dog_beast(ctx, message):
        """🐕"""
        if message.author.id == 206663073769979904:
            emoji = "🐕🇹🇭🇪🇧🇴🇾🇸☹️"
            for e in emoji:
                await message.add_reaction(e)
