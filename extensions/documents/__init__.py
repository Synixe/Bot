import argparse
import discord
import urllib.request
from . import parser

class BotExtension:
    def __init__(self, bot):
        self.name = "Documents"
        self.author = "Brett + nameless"
        self.version = "1.1"
        self.bot = bot

    def register(self):
        return {
            "rule": {
                "function": self.rule,
                "description": "Display a rule",
                "roles": ["@everyone"]
            },
            "rules": {
                "function": self.rules,
                "description": "Display the link to the rules",
                "roles": ["@everyone"]
            },
            "const": {
                "function": self.const,
                "description": "Display a section of the constitution",
                "roles": ["@everyone"]
            }
        }

    async def rule(self, args, message):
        parse = argparse.ArgumentParser(description="Display a rule")
        parse.add_argument("rule",help="Rule to display")
        args = parse.parse_args(args)
        req = urllib.request.Request(url="https://raw.githubusercontent.com/Synixe/Documents/master/SynixeRules.tex",headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
        with urllib.request.urlopen(req) as response:
            tex = parser.Parser(response.read().decode("UTF-8"))
        #try:
        rule = tex.getByID(args.rule)
        if isinstance(rule, str):
            await message.channel.send(tex.processRef(rule))
        elif isinstance(rule, dict):
            desc = ""
            if "text" in rule:
                desc = tex.processRef(rule["text"]) + "\n"
            if "subsections" in rule:
                x = 0
                for sub in rule["subsections"]:
                    x += 1
                    desc += "\n__{}.{} - {}__\n{}\n".format(args.rule.split(".")[0], x, sub["name"], tex.processRef(sub["text"]))
                    i = 0
                    for item in sub['items']:
                        i += 1
                        desc += "{}. {}\n".format(i, tex.processRef(item))
            i = 0
            for item in rule['items']:
                i += 1
                desc += "{}. {}\n".format(i, tex.processRef(item))
            embed = discord.Embed(
                title = args.rule + " " + rule["name"],
                description = desc,
                color = discord.Colour.from_rgb(r=255,g=192,b=60)
            )
            embed.set_author(
                name="Synixe Rules",
                url="https://github.com/Synixe/Documents/blob/master/SynixeRules.pdf",
                icon_url=self.bot.user.avatar_url
            )
            await message.channel.send(embed=embed)
        #except:
        #    await message.channel.send("There was an error finding that rule, it most likely doesn't exist.")

    async def rules(self, args, message):
        embed = discord.Embed(
            color = discord.Colour.from_rgb(r=255,g=192,b=60)
        )
        embed.set_author(
            name="Synixe Rules",
            url="https://github.com/Synixe/Documents/blob/master/SynixeRules.pdf",
            icon_url=self.bot.user.avatar_url
        )
        await message.channel.send(embed=embed)

    async def const(self, args, message):
        parse = argparse.ArgumentParser(description="Display a section of the constitution")
        parse.add_argument("section",nargs="?",help="Section to display")
        args = parse.parse_args(args)
        if args.section != None:
            req = urllib.request.Request(url="https://raw.githubusercontent.com/Synixe/Documents/master/SynixeConstitution.tex",headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
            with urllib.request.urlopen(req) as response:
                tex = parser.Parser(response.read().decode("UTF-8"))
            rule = tex.getByID(args.section)
            if isinstance(rule, str):
                await message.channel.send(rule)
            elif isinstance(rule, dict):
                desc = ""
                if "text" in rule:
                    desc = tex.processRef(rule["text"]) + "\n"
                if "subsections" in rule:
                    x = 0
                    for sub in rule["subsections"]:
                        x += 1
                        desc += "\n__{}.{} - {}__\n{}\n".format(args.section.split(".")[0], x, sub["name"], tex.processRef(sub["text"]))
                        i = 0
                        for item in sub['items']:
                            i += 1
                            desc += "{}. {}\n".format(i, tex.processRef(item))
                        y = 0
                        for ss in sub["subsubsections"]:
                            y += 1
                            desc += "\n*{}.{}.{} - {}*\n{}\n".format(args.section.split(".")[0], x, y, ss["name"], tex.processRef(ss["text"]))
                elif "subsubsections" in rule:
                    y = 0
                    for ss in rule["subsubsections"]:
                        y += 1
                        desc += "\n*{}.{}.{} - {}*\n{}\n".format(args.section.split(".")[0], args.section.split(".")[1], y, ss["name"], tex.processRef(ss["text"]))
                i = 0
                for item in rule['items']:
                    i += 1
                    desc += "{}. {}\n".format(i, tex.processRef(item))
                embed = discord.Embed(
                    title = args.section + " " + rule["name"],
                    description = desc,
                    color = discord.Colour.from_rgb(r=255,g=192,b=60)
                )
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
            embed = discord.Embed(
                color = discord.Colour.from_rgb(r=255,g=192,b=60)
            )
            embed.set_author(
                name="Synixe Constitution",
                url="https://github.com/Synixe/Documents/blob/master/SynixeConstitution.pdf",
                icon_url=self.bot.user.avatar_url
            )
            await message.channel.send(embed=embed)
