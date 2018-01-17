import argparse
import discord

class BotExtension:
    def __init__(self, bot):
        self.name = "Cards"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def register(self):
        return {
            "card" : {
                "function" : self.card,
                "description" : "Display a pretty card with information about a member",
                "roles" : ["@everyone"]
            }
        }

    async def card(self, args, message):
        parser = argparse.ArgumentParser(description="Display a pretty card with information about a member")
        parser.add_argument("user", nargs="?", default=str(message.author.id), help="The subject of the card. Defaults to the message's author.")
        args = parser.parse_args(args)
        user = message.channel.guild.get_member(self.bot.getIDFromTag(args.user))
        if user != None:
            embed = discord.Embed(
                title = user.name,
                color = user.colour
            )
            embed.add_field(name="Joined on",value=user.joined_at.strftime("%B %d, %Y"))
            embed.set_thumbnail(url=user.avatar_url)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Unable to find that user. Try using @ to mention them or use their Discord ID.")
