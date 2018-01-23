import discord
import logger

class BotExtension:
    def __init__(self, bot):
        self.name = "Server Monitor"
        self.author = "Brett"
        self.version = "1.0"

    async def post_to_bot_events(self, member, text):
        channel = discord.utils.find(lambda c: c.name == "botevents", member.guild.channels)
        if channel is not None:
            await channel.send(text)
        else:
            frame = getframeinfo(currentframe())
            logger.throw("Unable to find #botevents\n\t{0.filename} line {0.lineno - 4}".format(frame))

    async def on_member_join(self, member):
        await self.post_to_bot_events(member, "New Member: {0.display_name}#{0.discriminator} <@{0.id}> ({0.id})".format(member))

    async def on_member_remove(self, member):
        await self.post_to_bot_events(member, "Member left: {0.display_name}#{0.discriminator} <@{0.id}> ({0.id})".format(member))

    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            await self.post_to_bot_events(after, "<@{0.id}> {0.display_name} is now known as {1.display_name}".format(before, after))
