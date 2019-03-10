import discord
import bot

class Freeze(bot.Extension):
    @bot.role("moderator")
    @bot.argument("member+", discord.Member)
    @bot.command()
    async def freeze(ctx, message):
        """Freeze a user to prevent them from posting"""
        await ctx.args.member.add_roles(discord.utils.find(lambda m: m.name.lower() == "silenced", ctx.args.member.guild.roles))
        await message.add_reaction("✅")

    @bot.role("moderator")
    @bot.argument("member+", discord.Member)
    @bot.command()
    async def unfreeze(ctx, message):
        """Unfreeze a user and allow them to post again"""
        await ctx.args.member.remove_roles(discord.utils.find(lambda m: m.name.lower() == "silenced", ctx.args.member.guild.roles))
        await message.add_reaction("✅")
