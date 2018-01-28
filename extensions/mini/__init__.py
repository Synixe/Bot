import argparse
import discord
import random
#import gifs
#from textblob import TextBlob

class BotExtension:
    def __init__(self, bot):
        self.name = "Mini Commands"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot


    def register(self):
        return {
            "dice" : {
                "function" : self.dice,
                "description" : "Roll a dice",
                "roles" : ["@everyone"]
            }
        }

    async def dice(self, args, message):
        parser = argparse.ArgumentParser(description="Roll a dice")
        parser.add_argument("n",nargs="?",type=int,default=6,help="Number of sides")
        args = parser.parse_args(args)
        value = random.randint(1,args.n)
        messages = ["The value is {0}","You rolled a {0}","It lands on {0}"]
        await message.channel.send(self.bot.processOutput(random.choice(messages).format(value),message))

    #async def on_message(self, message):
    #    original = TextBlob(message.content)
    #    fixed = original.correct()
    #    diff = list(set(original.words) - set(fixed.words))
    #    for r in ["hey","devis","namless","m8","boi"]:
    #        if r in diff:
    #            diff.remove(r)
    #        elif r.upper() in diff:
    #            diff.remove(r.upper())
    #        elif r.title() in diff:
    #            diff.remove(r.title())
    #    if len(diff) >= 3:
    #        async with message.channel.typing():
    #            await message.channel.send(file=discord.File(fp=gifs.getRandom("spelling")))
