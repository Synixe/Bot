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
        g = member.guild
        for c in g.channels:
            if c.name == "lobby":
                l = c
            elif c.name == "info":
                i = c
            elif c.name == "events":
                e = c
            elif c.name == "repohelp":
                r = c
        await l.send("<@"+str(member.id) + ">! Welcome to Synixe! Here is some basic info about our group: If you check out <#"+str(e.id)+"> you can see our upcoming missions. We play at 7pm PST / 10pm EST. We have some mods you'll need to download from <#"+str(i.id)+">. If you have any questions while getting those setup we're more than happy to help in <#"+str(r.id)+">.")
        await member.add_roles(self.getRole(g, "new"))

    async def on_member_remove(self, member):
        await self.post_to_bot_events(member, "Member left: {0.display_name}#{0.discriminator} <@{0.id}> ({0.id})".format(member))

    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            await self.post_to_bot_events(after, "<@{0.id}> {0.display_name} is now known as {1.display_name}".format(before, after))

    async def on_member_ban(self, g, member):
        await self.post_to_bot_events("<@"+str(member.id) + "> ("+member.name+"#"+member.discriminator+") has been banned.")

    async def on_member_unban(self, g, member):
        await self.post_to_bot_events("<@"+str(member.id) + "> ("+member.name+"#"+member.discriminator+") has been unbanned.")


    def getRole(self, guild, name):
        for r in guild.roles:
            if name.lower() == r.name.lower():
                return r
        return None
