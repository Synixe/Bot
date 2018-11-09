import discord
import urllib.request

import bot
from . import parser

class Documents(bot.Extension):
    @bot.argument("rule")
    @bot.command()
    async def rule(ctx, message):
        """Display a rule"""
        try:
            embed = get_from_latex(
                "https://raw.githubusercontent.com/Synixe/Documents/master/SynixeRules.tex",
                ctx.args.rule
            )
        except IndexError:
            await message.channel.send("That rule does not exist.")
            return
        if embed != None:
            if isinstance(embed, discord.Embed):
                embed.set_author(
                    name="Synixe Rules",
                    url="http://synixe.com/rules.html",
                    icon_url=ctx.bot.user.avatar_url
                )
                try:
                    await message.channel.send(embed=embed)
                except discord.errors.HTTPException:
                    await message.channel.send("That section is too large, you'll need to be more specific")
            else:
                await message.channel.send(embed)

    @bot.argument("section")
    @bot.command()
    async def const(ctx, message):
        """Get a section from the Constitution"""
        try:
            embed = get_from_latex(
                "https://raw.githubusercontent.com/Synixe/Documents/master/SynixeConstitution.tex",
                ctx.args.section
            )
        except IndexError:
            await message.channel.send("That section does not exist.")
            return
        if embed != None:
            if isinstance(embed, discord.Embed):
                embed.set_author(
                    name="Synixe Constitution",
                    url="http://synixe.com/const.html",
                    icon_url=ctx.bot.user.avatar_url
                )
                try:
                    await message.channel.send(embed=embed)
                except discord.errors.HTTPException:
                    await message.channel.send("That section is too large, you'll need to be more specific")
            else:
                await message.chanel.send(embed)

def get_from_latex(url, section):
    """Get a section from the rules"""
    req = urllib.request.Request(url=url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
    with urllib.request.urlopen(req) as response:
        tex = parser.Parser(response.read().decode("UTF-8"))
    rule = tex.get_from_id(section)
    if isinstance(rule, str):
        return rule
    elif isinstance(rule, dict):
        desc = ""
        if "text" in rule:
            desc = tex.process_ref(rule["text"]) + "\n"
        if "subsections" in rule:
            x = 0
            for sub in rule["subsections"]:
                x += 1
                desc += "\n__{}.{} - {}__\n{}\n".format(section.split(".")[0], x, sub["name"], tex.process_ref(sub["text"]))
                i = 0
                for item in sub['items']:
                    i += 1
                    desc += f"{i}. {tex.process_ref(item)}\n"
                y = 0
                for ss in sub["subsubsections"]:
                    y += 1
                    desc += "\n*{}.{}.{} - {}*\n{}\n".format(section.split(".")[0], x, y, ss["name"], tex.process_ref(ss["text"]))
        elif "subsubsections" in rule:
            y = 0
            for ss in rule["subsubsections"]:
                y += 1
                desc += "\n*{}.{}.{} - {}*\n{}\n".format(section.split(".")[0], section.split(".")[1], y, ss["name"], tex.process_ref(ss["text"]))
        i = 0
        for item in rule['items']:
            i += 1
            desc += f"{i}. {tex.process_ref(item)}\n"
        embed = discord.Embed(
            title=section + " " + rule["name"],
            description=desc,
            color=discord.Colour.from_rgb(r=255, g=192, b=60)
        )
        return embed
