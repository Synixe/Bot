"""Creating Polls for Disco"""
import discord
import bot

class Polls(bot.Extension):
    """Polls for Disco"""

    @bot.role("active")
    @bot.argument("(title)")
    @bot.argument("text+")
    @bot.command()
    async def poll(ctx, message):
        """Birth of Polls"""
        if ctx.args.title == None:
            msg = await message.channel.send(" ".join(ctx.args.text))
        else:
            embed = discord.Embed(
                title=ctx.args.title,
                color=discord.Colour.from_rgb(r=255, g=192, b=60),
                description=ctx.args.text
            )
            embed.set_footer(text="Created by: {}".format(message.author.display_name))
            msg = await message.channel.send(embed=embed)
        await message.delete()
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
