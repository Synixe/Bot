import bot
import discord

class Profiles(bot.Extension):

    @bot.argument("member+", discord.Member)
    @bot.command()
    async def avatar(ctx, message):
        """Prints out a users discord avatar"""
        embed = discord.Embed(
            color=ctx.args.member.color
        )
        embed.set_author(
            name=ctx.args.member.display_name,
            url=ctx.args.member.avatar_url
        )
        embed.set_image(url=ctx.args.member.avatar_url)
        await message.channel.send(embed=embed)
