"""Synixe Rules and Constitution"""
import argparse
import discord
import urllib.request
from . import parser

class BotExtension:
    """Synixe Rules and Constitution"""
    def __init__(self, bot):
        self.name = "Documents"
        self.author = "Brett + nameless"
        self.version = "1.1"
        self.bot = bot

    def __register__(self):
        return {
            "rule": {
                "function": self.rule,
                "roles": ["@everyone"]
            },
            "rules": {
                "function": self.rules,
                "roles": ["@everyone"]
            },
            "const": {
                "function": self.const,
                "roles": ["@everyone"]
            }
        }

    async def rule(self, args, message):
        """Display a rule"""
        parse = argparse.ArgumentParser(description=self.rule.__doc__)
        parse.add_argument("rule", help="Rule to display")
        args = await self.bot.parse_args(parse, args, message)
        if args != False:
            try:
                embed = self.get_from_latex(
                    "https://raw.githubusercontent.com/Synixe/Documents/master/SynixeRules.tex",
                    args.rule
                )
            except IndexError:
                await message.channel.send("That rule does not exist.")
                return
            if embed != None:
                if isinstance(embed, discord.Embed):
                    embed.set_author(
                        name="Synixe Rules",
                        url="https://github.com/Synixe/Documents/blob/master/SynixeRules.pdf",
                        icon_url=self.bot.user.avatar_url
                    )
                    try:
                        await message.channel.send(embed=embed)
                    except discord.errors.HTTPException:
                        await message.channel.send("That section is too large, you'll need to be more specific")
                else:
                    await message.chanel.send(embed)

    async def rules(self, args, message):
        """Display the link to the rules"""
        if not len(args) == 0:
            await message.channel.send("Use {}rule".format(self.bot.prefix))
            return
        embed = discord.Embed(
            color=discord.Colour.from_rgb(r=255, g=192, b=60)
        )
        embed.set_author(
            name="Synixe Rules",
            url="https://github.com/Synixe/Documents/blob/master/SynixeRules.pdf",
            icon_url=self.bot.user.avatar_url
        )
        await message.channel.send(embed=embed)

    async def const(self, args, message):
        """Display a section of the constitution"""
        parse = argparse.ArgumentParser(description=self.const.__doc__)
        parse.add_argument("section", nargs="?", help="Section to display")
        args = await self.bot.parse_args(parse, args, message)
        if args != False:
            if args.section != None:
                embed = self.get_from_latex(
                    "https://raw.githubusercontent.com/Synixe/Documents/master/SynixeConstitution.tex",
                    args.section
                )
                if embed != None:
                    if isinstance(embed, discord.Embed):
                        embed.set_author(
                            name="Synixe Constitution",
                            url="https://github.com/Synixe/Documents/blob/master/SynixeConstitution.pdf",
                            icon_url=self.bot.user.avatar_url
                        )
                        try:
                            await message.channel.send(embed=embed)
                        except discord.errors.HTTPException:
                            await message.channel.send("That section is too large, you'll need to be more specific")
                    else:
                        await message.chanel.send(embed)
            else:
                embed = discord.Embed(
                    color = discord.Colour.from_rgb(r=255,g=192,b=60)
                )
                embed.set_author(
                    name="Synixe Constitution",
                    url="https://github.com/Synixe/Documents/blob/master/SynixeConstitution.pdf",
                    icon_url=self.bot.user.avatar_url
                )
                await message.channel.send(embed=embed)

    @classmethod
    def get_from_latex(cls, url, section):
        """Get a discord embed from latex"""
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
                    desc += "\n__{}.{} - {}__\n{}\n".format(args.section.split(".")[0], x, sub["name"], tex.process_ref(sub["text"]))
                    i = 0
                    for item in sub['items']:
                        i += 1
                        desc += "{}. {}\n".format(i, tex.process_ref(item))
                    y = 0
                    for ss in sub["subsubsections"]:
                        y += 1
                        desc += "\n*{}.{}.{} - {}*\n{}\n".format(args.section.split(".")[0], x, y, ss["name"], tex.process_ref(ss["text"]))
            elif "subsubsections" in rule:
                y = 0
                for ss in rule["subsubsections"]:
                    y += 1
                    desc += "\n*{}.{}.{} - {}*\n{}\n".format(args.section.split(".")[0], args.section.split(".")[1], y, ss["name"], tex.process_ref(ss["text"]))
            i = 0
            for item in rule['items']:
                i += 1
                desc += "{}. {}\n".format(i, tex.process_ref(item))
            embed = discord.Embed(
                title=section + " " + rule["name"],
                description=desc,
                color=discord.Colour.from_rgb(r=255, g=192, b=60)
            )
            return embed
