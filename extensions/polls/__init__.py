import discord
import argparse

class BotExtension:
    """Adds polls to the bot"""
    def __init__(self, bot):
        self.bot = bot
        self.name = "Poll"
        self.author = "nameless + Brett"
        self.version = "1.0"

    def register(self):
        """Register with the main bot"""
        return {
            "poll" : {
                "function": self.poll,
                "roles" : ["active", "new", "inactive"]
            }
        }

    async def poll(self, args, message):
        """Create a poll"""
        parser = argparse.ArgumentParser(description=self.poll.__doc__)
        parser.add_argument(
            "-t", "--title", default=None, help="Title of the poll"
        )
        parser.add_argument("text", nargs="+", help="Text of the poll")
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            if args.title == None:
                msg = await message.channel.send(" ".join(args.text))
            else:
                embed = discord.Embed(
                    title=args.title,
                    color=discord.Colour.from_rgb(r=255, g=192, b=60),
                    description=" ".join(args.text)
                )
                msg = await message.channel.send(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
