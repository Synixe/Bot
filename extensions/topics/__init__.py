import argparse

class BotExtension:
    def __init__(self, bot):
        self.name = "Topics"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot
        self.topics = {"R6S": "Rainbow 6 Siege", "ED": "Elite: Dangerous", "PUBG": "PUBG"}

    def register(self):
        return {
            "sub" : {
                "function" : self.sub,
                "roles" : ["active","new"]
            },
            "unsub" : {
                "function" : self.unsub,
                "roles" : ["active","new"]
            }
        }

    async def sub(self, args, message):
        """Subscribe to a topic"""
        parser = argparse.ArgumentParser(description=self.sub.__doc__)
        parser.add_argument("topic", nargs="?",help=self.bot.processOutput("Topic to subscribe to.", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            if args.topic == None:
                text = "Topics:\n"
                for topic in self.topics:
                    text += "**" + topic + "** - " + self.topics[topic] + "\n"
                await message.channel.send(text)
            else:
                if args.topic.upper() in self.topics:
                    await message.author.add_roles(self.getRole(message.channel.guild, self.topics[args.topic.upper()]))
                    await message.delete()
                else:
                    await message.channel.send(self.bot.processOutput("That topic doesn't exist", message))

    async def unsub(self, args, message):
        """Unsubscribe from a topic"""
        parser = argparse.ArgumentParser(description=self.unsub.__doc__)
        parser.add_argument("topic", nargs="?",help=self.bot.processOutput("Topic to unsubscribe from", message))
        args = await self.bot.parseArgs(parser, args, message)
        if args != False:
            if args.topic == None:
                await message.channel.send(self.bot.processOutput("No topic specified!", message))
            else:
                if args.topic.upper() in self.topics:
                    await message.author.remove_roles(self.getRole(message.channel.guild, self.topics[args.topic.upper()]))
                    await message.channel.send(self.bot.processOutput("Unsubscribed!", message))
                else:
                    await message.channel.send(self.bot.processOutput("That topic doesn't exist", message))

    def getRole(self, guild, name):
        for r in guild.roles:
            if name.lower() == r.name.lower():
                return r
        return None
