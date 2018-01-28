import argparse
import discord
from textblob import TextBlob

class BotExtension:
    def __init__(self, bot):
        self.name = "Policer"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot
        self.active = False

        self.history = {}

    def register(self):
        return {
            "niceness" : {
                "function" : self.niceness,
                "description" : "How nice a person speaks",
                "roles" : ["@everyone"]
            }
        }

    async def niceness(self, args, message):
        parser = argparse.ArgumentParser(description="How nice a user is.")
        parser.add_argument("user", nargs="?", default=str(message.author.id), help="The user to analyze")
        args = parser.parse_args(args)
        user = message.channel.guild.get_member(self.bot.getIDFromTag(args.user))
        if user != None:
            try:
                niceness = self.history[user.id]
                if niceness >= 0.9:
                    await message.channel.send(self.bot.processOutput("Wow! Looking at their history. {0.display_name} is extremely nice".format(user),message))
                elif niceness >= 0.5:
                    await message.channel.send(self.bot.processOutput("They're a really positive person!",message))
                elif niceness >= 0:
                    await message.channel.send(self.bot.processOutput("They mostly say nice things, mostly.",message))
                elif niceness >= 0.3:
                    await message.channel.send(self.bot.processOutput("They look like a negative person...",message))
                else:
                    await message.channel.send(self.bot.processOutput("Please don't make me read their history again :cry:",message))
            except:
                await message.channel.send(self.bot.processOutput("I can't figure it out yet, but I'm getting smarter",message))
        else:
            await message.channel.send(self.bot.processOutput("Unable to find that user. Try using @ to mention them or use their Discord ID.",message))


    async def on_message(self, message):
        if message.content == "nameless":
            await message.channel.send("NEW ZEALAND NAMES LUL")
            return
        text = TextBlob(message.content)
        polarity = text.sentiment.polarity
        if "bad" in message.content:
            polarity += 0.3
        if polarity <= -0.5:
            await message.channel.send(self.bot.processOutput("There is no need to talk with such negativity.",message))
        try:
            self.history[message.author.id] += text.sentiment.polarity
        except:
            self.history[message.author.id] = text.sentiment.polarity
