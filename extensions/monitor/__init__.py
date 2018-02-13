import discord
import logger

class BotExtension:
    def __init__(self, bot):
        self.name = "Server Monitor"
        self.author = "Brett + nameless"
        self.version = "1.1"
        self.bot = bot
        self.disable_during_test = True

    async def post_to_bot_events(self, member, text):
        channel = discord.utils.find(lambda c: c.name == "botevents", member.guild.channels)
        if channel is not None:
            await channel.send(text)

    async def on_member_join(self, member):
        #await self.post_to_bot_events(member, "New Member: {0.display_name}#{0.discriminator} <@{0.id}> ({0.id})".format(member))
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
            channel = discord.utils.find(lambda c: c.name == "botevents", after.guild.channels)
            if channel != None:
                embed = discord.Embed(
                    title = "Nickname Change",
                    color = discord.Colour.from_rgb(r=255,g=192,b=60)
                )
                embed.add_field(name="Previous Name", value=before.display_name)
                embed.add_field(name="New Name", value=after.display_name)
                await channel.send(embed=embed)

    async def on_member_ban(self, g, member):
        await self.post_to_bot_events(member, "<@{0.id}> ({0.name}#{0.discriminator}) has been banned.".format(member))

    async def on_member_unban(self, g, member):
        await self.post_to_bot_events(member, "<@{0.id}> ({0.name}#{0.discriminator}) has been unbanned.".format(member))

    def getRole(self, guild, name):
        for r in guild.roles:
            if name.lower() == r.name.lower():
                return r
        return None
