"""Topic System for games other than Arma"""

import argparse

class BotExtension:
    """Topic System for games other than Arma"""
    def __init__(self, bot):
        self.name = "Topics"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot
        self.topics = {
            "R6S": "Rainbow 6 Siege",
            "ED": "Elite: Dangerous",
            "LOL": "League of Legends",
            "ASTRO": "Astroneer"
        }

    def __register__(self):
        return {
            "sub" : {
                "function" : self.sub,
                "roles" : ["active", "new"]
            },
            "unsub" : {
                "function" : self.unsub,
                "roles" : ["active", "new"]
            }
        }

    async def sub(self, args, message):
        """Subscribe to a topic"""
        parser = argparse.ArgumentParser(description=self.sub.__doc__)
        parser.add_argument("topic", nargs="?", help="Topic to subscribe to.")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            if args.topic == None:
                text = "Topics:\n"
                for topic in self.topics:
                    text += "**" + topic + "** - " + self.topics[topic] + "\n"
                await message.channel.send(text)
            else:
                if args.topic.upper() in self.topics:
                    await message.author.add_roles(self.getRole(
                        message.channel.guild,
                        self.topics[args.topic.upper()]
                    ))
                    await message.delete()
                else:
                    await message.channel.send("That topic doesn't exist")

    async def unsub(self, args, message):
        """Unsubscribe from a topic"""
        parser = argparse.ArgumentParser(description=self.unsub.__doc__)
        parser.add_argument("topic", nargs="?", help="Topic to unsubscribe from")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            if args.topic == None:
                await message.channel.send("No topic specified!")
            else:
                if args.topic.upper() in self.topics:
                    await message.author.remove_roles(self.getRole(
                        message.channel.guild, self.topics[args.topic.upper()]
                    ))
                    await message.delete()
                else:
                    await message.channel.send("That topic doesn't exist")

    @classmethod
    def getRole(cls, guild, name):
        """Get a role by name"""
        for role in guild.roles:
            if name.lower() == role.name.lower():
                return role
        return None
