"""Teamspeak for Disco"""
import discord
import bot

class TeamSpeak(bot.Extension):
    """Provides TeamSpeak commands"""
    @bot.argument("member+", discord.Member)
    @bot.command()
    async def ts(ctx, message):
        """Sends a user the TeamSpeak info in a direct message"""
        await ctx.args.member.send("TeamSpeak Server: ts.synixe.com")
        await message.add_reaction("✅")

    @bot.event("on_message")
    async def delete_ts(ctx, message):
        """Deletes any messages containing the TeamSpeak Server"""
        if "ts.synixe.com" in message.content.lower().replace(" ", ""):
            await message.channel.send("Please don't post the TeamSpeak Server, a member of @Active can use {}ts to send someone the server.".format(ctx.profile.prefix))
            await message.delete()
