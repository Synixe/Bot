import discord
import bot

class NamelessText(bot.Extension):
    @bot.event("on_message")
    async def replace_nameless(ctx, message):
        """Deletes any messages containing nameless and replaces it with Nameless"""
        if "nameless" in message.content.replace(" ", ""):
            await message.channel.send("{}\n There, fixed that for ya".format(message.content.replace("nameless", "Nameless")))
            await message.delete()
