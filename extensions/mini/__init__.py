import argparse
import discord
import random

class BotExtension:
    def __init__(self, bot):
        self.name = "Mini Commands"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot
        self.topics = {"R6S": "Rainbow 6 Siege", "ED": "Elite: Dangerous", "PUBG": "PUBG"}

    def register(self):
        return {
            "dice" : {
                "function" : self.dice,
                "description" : "Roll a dice",
                "roles" : ["@everyone"]
            },
            "flip" : {
                "function" : self.flip,
                "description" : "flip a coin",
                "roles" : ["@everyone"]
            },
            "card" : {
                "function" : self.card,
                "description" : "Display a pretty card with information about a member",
                "roles" : ["active","new","inactive"]
            },
            "ping" : {
                "function" : self.ping,
                "description" : "Ping the bot for a response",
                "roles" : ["@everyone"]
            }
        }

    async def dice(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Roll a dice", message))
        parser.add_argument("n",nargs="?",type=int,default=6,help=self.bot.processOutput("Number of sides", message))
        args = parser.parse_args(args)
        value = random.randint(1,args.n)
        messages = ["The value is {0}","You rolled a {0}","It lands on {0}"]
        await message.channel.send(self.bot.processOutput(random.choice(messages).format(value),message))

    async def flip(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Flip a coin", message))
        args = parser.parse_args(args)
        side = random.randint(0,1)
        if side == 0:
            output = "It lands on heads"
        else:
            output = "It lands on tails"
        await message.channel.send(self.bot.processOutput(output, message))

    async def card(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Display a pretty card with information about a member", message))
        parser.add_argument("user", nargs="?", default=str(message.author.id), help=self.bot.processOutput("The subject of the card. Defaults to the message's author.", message))
        args = parser.parse_args(args)
        user = message.channel.guild.get_member(self.bot.getIDFromTag(args.user))
        if user != None:
            embed = discord.Embed(
                title = user.name,
                color = user.colour
            )
            embed.add_field(name=self.bot.processOutput("Joined on", message),value=user.joined_at.strftime("%B %d, %Y"))
            embed.set_thumbnail(url=user.avatar_url)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(self.bot.processOutput("Unable to find that user. Try using @ to mention them or use their Discord ID.", message))

    async def ping(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Ping the bot", message))
        args = parser.parse_args(args)
        await message.channel.send("{:0.0f}ms".format(self.bot.latency * 1000))

    def getRole(self, guild, name):
        for r in guild.roles:
            if name.lower() == r.name.lower():
                return r
        return None
