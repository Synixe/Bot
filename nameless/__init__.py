import discord
import bot

class NamelessText(bot.Extension):
    @bot.event("on_message")
    async def replace_nameless(ctx, message):
        """Deletes any messages containing nameless and replaces it with Nameless"""
        if "nameless" in message.content:
            await message.channel.send("{}\nThere, fixed that for ya".format(message.content.replace("nameless", "Nameless")))
