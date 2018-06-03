"""Creating Polls for Disco"""
import discord
import bot

class Polls(bot.Extension):
    """Polls for Disco"""

    @bot.role("active")
    @bot.role("new")
    @bot.role("inactive")
    @bot.argument("(title)")
    @bot.argument("text+")
    @bot.command()
    async def poll(ctx, message):
        """Birth of Polls"""
        print(ctx.args.title)
        if ctx.args.title == None:
            msg = await message.channel.send(ctx.args.text)
        else:
            embed = discord.Embed(
                title=ctx.args.title,
                color=discord.Colour.from_rgb(r=255, g=192, b=60),
                description=" ".join(ctx.args.text)
            )
            msg = await message.channel.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
