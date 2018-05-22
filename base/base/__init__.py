import bot
import discord

import os

class Info(bot.Extension):
    """Provides information about the Bot and loaded extensions"""

    @bot.argument("[command]", bot.Command)
    @bot.command()
    async def info(ctx, message):
        """Displays info about the bot or a command"""
        if ctx.args.command == None:
            embed = discord.Embed()
            embed.add_field(name="Profile", value=ctx.profile.name)
            embed.add_field(name="Mode", value=ctx.profile.mode)
            embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar_url)
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="{0.profile.prefix}{0.args.command.name} {0.args.command.usage}".format(ctx),
                description=ctx.args.command.help,
                url="https://github.com/Synixe/Bot/blame/master/{0}#L{1.start}L{1.end}".format(ctx.args.command.file.replace(os.getcwd(), ""), ctx.args.command)
            )
            embed.set_footer(text=ctx.args.command.extension.fullname + "." + ctx.args.command.name)
            await message.channel.send(embed=embed)
