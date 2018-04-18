"""Help"""
import argparse
import discord
import math

class BotExtension:
    """Help"""
    def __init__(self, bot):
        self.name = "Help"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

        self.helpids = []

        self.commands = []
        self.names = []

    def __register__(self):
        return {
            "help" : {
                "function": self.helpfunc,
                "roles": ["@everyone"]
            }
        }

    async def helpfunc(self, args, message):
        """Help"""
        if self.commands == []:
            for c in self.bot.commands:
                self.names.append(c)
                self.commands.append(self.bot.commands[c])
        parser = argparse.ArgumentParser(description=self.helpfunc.__doc__)
        parser.add_argument("command", nargs="?", help="Command to look up")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            if args.command != None:
                await message.channel.send("meh")
            else:
                m = "```makefile\n"
                for i in range(0,6):
                    m += self.names[i]+":\n    " + self.commands[i]["function"].__doc__+"\n"
                embed = discord.Embed(
                    title="Command Browser",
                    description=m+"```",
                    color=discord.Colour.from_rgb(r=255, g=192, b=60)
                )
                embed.set_footer(text="Page: 1")
                mid = await message.channel.send(embed=embed)
                await mid.add_reaction("\u2B05")
                await mid.add_reaction("\u27A1")
                await mid.add_reaction("❌")
                self.helpids.append(mid.id)

    async def on_reaction_add(self, reaction, member):
        """Make the help dialog work"""
        if member.id == self.bot.user.id:
            return
        if reaction.message.id in self.helpids:
            if reaction.emoji == "❌":
                await reaction.message.edit(content="Help Closed", embed=None)
                return
            page = int(reaction.message.embeds[0].footer.text.split(" ")[-1])
            if reaction.emoji == "⬅":
                page -= 1
            elif reaction.emoji == "➡":
                page += 1

            if page == 0:
                page = math.ceil(len(self.commands) / 6)
            if page > math.ceil(len(self.commands) / 6):
                page = 1

            m = "```makefile\n"
            for i in range(0 + (6 * (page - 1)),6 * (page)):
                try:
                    m += self.names[i]+":\n    " + self.commands[i]["function"].__doc__+"\n"
                except IndexError:
                    pass
            embed = discord.Embed(
                title="Command Browser",
                description=m+"```",
                color=discord.Colour.from_rgb(r=255, g=192, b=60)
            )
            embed.set_footer(text="Page: "+str(page))
            await reaction.message.clear_reactions()
            await reaction.message.edit(embed=embed)
            await reaction.message.add_reaction("\u2B05")
            await reaction.message.add_reaction("\u27A1")
            await reaction.message.add_reaction("❌")
