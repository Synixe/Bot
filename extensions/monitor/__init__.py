"""Monitor the server for changes"""
import pymysql
import discord
import tokens
import logger

class BotExtension:
    """Monitor the server for changes"""
    def __init__(self, bot):
        self.name = "Server Monitor"
        self.author = "Brett + nameless"
        self.version = "1.1"
        self.bot = bot
        self.disable_during_test = False

    async def post_to_bot_events(self, member, text):
        """Post a message to #botevents"""
        channel = discord.utils.find(lambda c: c.name == "botevents", member.guild.channels)
        if channel is not None:
            await channel.send(text)

    @classmethod
    def get_connection(cls):
        """Gets a connection to the database"""
        return pymysql.connect(
            host=tokens.MYSQL.HOST,
            user=tokens.MYSQL.USER,
            password=tokens.MYSQL.PASS,
            db=tokens.MYSQL.DATA,
            cursorclass=pymysql.cursors.DictCursor
        )

    def insert(self, event_type, content):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `bot_events` (`type`, `content`) VALUES (%s, %s)"
                cursor.execute(sql, (event_type, content ))
                connection.commit()
        finally:
            connection.close()

    async def on_member_join(self, member):
        self.insert('member_join', str(member.id))
        """Print a welcome message to new members"""
        guild = member.guild
        for channel in guild.channels:
            if channel.name == "lobby":
                lobby = channel
            elif channel.name == "info":
                info = channel
            elif channel.name == "events":
                events = channel
            elif channel.name == "repohelp":
                repohelp = channel
        await lobby.send(
            ("<@{}>! Welcome to Synixe!"+
            "Here is some basic info about our group: "+
            "If you check out <#{}> you can see our upcoming missions. "+
            "We play at 7pm PST / 10pm EST. "+
            "We have some mods you'll need to download from <#{}>. "+
            "If you have any questions while getting those setup we're more than "+
            "happy to help in <#{}>.").format(member, events, info, repohelp)
        )
        await member.add_roles(self.get_role(g, "new"))

    async def on_member_remove(self, member):
        self.insert('member_remove', str(member.id))
        """Post a message in #botevents when someone leaves the server"""
        await self.post_to_bot_events(
            member,
            "Member left: {0.display_name}#{0.discriminator} <@{0.id}> ({0.id})".format(member)
        )

    async def on_member_update(self, before, after):
        """Post a message in #botevents when someone leaves the server"""
        if before.display_name != after.display_name:
            self.insert('member_update_name', str(after.id)+"::"+before.display_name+"::"+after.display_name)
            channel = discord.utils.find(lambda c: c.name == "botevents", after.guild.channels)
            if channel != None:
                embed = discord.Embed(
                    title="Nickname Change",
                    color=discord.Colour.from_rgb(r=255,g=192,b=60)
                )
                embed.add_field(name="Previous Name", value=before.display_name)
                embed.add_field(name="New Name", value=after.display_name)
                await channel.send(embed=embed)

    async def on_member_ban(self, _, member):
        self.insert('member_ban', str(after.id))
        """Post a message in #botevents when someone is banned"""
        await self.post_to_bot_events(
            member,
            "<@{0.id}> ({0.name}#{0.discriminator}) has been banned.".format(member)
        )

    async def on_member_unban(self, _, member):
        self.insert('member_unban', str(after.id))
        """Post a message in #botevents when someone is unbanned"""
        await self.post_to_bot_events(
            member,
            "<@{0.id}> ({0.name}#{0.discriminator}) has been unbanned.".format(member)
        )

    @classmethod
    def get_role(cls, guild, name):
        """Get role by name"""
        for role in guild.roles:
            if name.lower() == role.name.lower():
                return role
        return None
