import discord
import bot

class Anon(bot.Extension):
    @bot.argument("text+")
    @bot.command()
    async def anon(ctx, message):
        """Send a message to the Managers anonymously"""
        if not isinstance(message.channel, discord.DMChannel):
            await message.delete()
            await message.channel.send("Only use this command in a direct message.")
        else:
            channel = discord.utils.find(lambda c: c.name == "inbox", discord.utils.find(lambda g: g.name == "Synixe", ctx.bot.guilds).channels)
            if channel is not None:
                await channel.send(ctx.args.text)
                await message.add_reaction("✅")
