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
                "description" : "Subscribe to a topic",
                "roles" : ["active","new"]
            },
            "unsub" : {
                "function" : self.unsub,
                "description" : "Unsubscribe from a topic",
                "roles" : ["active","new"]
            }
        }

    async def sub(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Subscribe to a topic", message))
        parser.add_argument("topic", nargs="?",help=self.bot.processOutput("Topic to subscribe to.", message))
        args = parser.parse_args(args)
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
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Unsubscribe from a topic", message))
        parser.add_argument("topic", nargs="?",help=self.bot.processOutput("Topic to unsubscribe from", message))
        args = parser.parse_args(args)
        if args.topic == None:
            await message.channel.send(self.bot.processOutput("No topic specified!", message))
        else:
            if args.topic.upper() in self.topics:
                await message.author.remove_roles(self.getRole(message.channel.guild, self.topics[args.topic.upper()]))
                await message.channel.send(self.bot.processOutput("Unsubscribed!", message))
            else:
                await message.channel.send(self.bot.processOutput("That topic doesn't exist", message))
