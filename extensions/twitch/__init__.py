"""Twitch Extension"""
import random
import discord
import logger

class BotExtension:
    """Twitch Extension"""
    def __init__(self, bot):
        self.name = "Twitch"
        self.author = "Brett + nameless"
        self.version = "1.0"
        self.bot = bot
        self.disable_during_test = True

    async def on_member_update(self, before, after):
        """Posts to #streams if a user starts streaming"""
        if self.bot.in_role_list(after, ["active"]):
            if after.activity != None and isinstance(after.activity, discord.Streaming):
                print(after.activity.details)
                if before.activity == None or not isinstance(before.activity, discord.Streaming):
                    channel = discord.utils.find(lambda c: c.name == "streams", after.guild.channels)
                    if channel != None:
                        lines = open('./extensions/twitch/taglines.txt').read().splitlines()
                        embed = discord.Embed(
                            title=after.activity.name,
                            url=after.activity.url,
                            description=after.activity.details,
                            color=discord.Colour.from_rgb(r=255, g=192, b=60)
                        )
                        embed.set_author(name=after.display_name)
                        embed.set_thumbnail(url=after.avatar_url)
                        await channel.send(embed=embed, content=random.choice(lines).format(after.display_name))
                    else:
                        logger.error("Unable to find #bot")
