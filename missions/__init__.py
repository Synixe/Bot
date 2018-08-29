import pymysql
import discord
import bot

class Slotting(bot.Extension):
    """Provides commands for Slotting"""

    @bot.argument("role", str)
    @bot.command()
    async def slot(ctx, message):
        """Slot into a role for a mission"""
        if ";" in ctx.args.role:
            return
        channel = discord.utils.find(lambda c: c.name == "events", message.channel.guild.channels)
        if channel is not None:
            event_id = 0
            target = None
            messages = channel.history(limit=10)
            async for msg in messages:
                if len(msg.embeds) == 1:
                    try:
                        if msg.embeds[0].footer.text.startswith("Mission ID:"):
                            event_id = int(msg.embeds[0].footer.text.split(": ")[1])
                            target = msg
                    except AttributeError:
                        pass
            if target != None:
                connection = get_connection(ctx)
                try:
                    with connection.cursor() as cursor:
                        sql = f"SELECT * FROM `slots` WHERE (`event` = '{str(event_id)}') AND (LOWER(`name`) LIKE '%{ctx.args.role.lower()}%') AND (`playerid` IS NULL)"
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        if data:
                            slot = data[0]
                            sql = "UPDATE `slots` SET `playerid` = NULL WHERE `playerid` = '"+str(message.author.id)+"'"
                            cursor.execute(sql)
                            sql = "UPDATE `slots` SET `playerid` = '"+str(message.author.id)+"' WHERE `id` = '"+str(slot['id'])+"'"
                            cursor.execute(sql)
                            connection.commit()
                            await display_event(ctx, target, event_id, message)
                            await message.add_reaction("✅")
                        else:
                            await message.channel.send("🤔 That role was not found for {}.".format(target.embeds[0].title))
                finally:
                    connection.close()

class MissionMakers(bot.Extension):
    """Provides commands for MissionMakers"""

    @bot.role("missionmaker")
    @bot.argument("event", int)
    @bot.command()
    async def post(ctx, message):
        """Post an event to #events"""
        channel = discord.utils.find(lambda c: c.name == "events", message.channel.guild.channels)
        if channel is not None:
            mid = await channel.send("New Mission Posted!")
            await display_event(ctx, mid, ctx.args.event, message)
            await message.add_reaction("✅")

def get_connection(ctx):
    """Gets a connection to the database"""
    return pymysql.connect(
        host=ctx.profile.tokens['mysql']['host'],
        user=ctx.profile.tokens['mysql']['user'],
        password=ctx.profile.tokens['mysql']['pass'],
        db=ctx.profile.tokens['mysql']['data'],
        cursorclass=pymysql.cursors.DictCursor
    )

async def display_event(ctx, target, event, message):
    """Display an event sheet in #events"""
    connection = get_connection(ctx)
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM `events` WHERE `id` = '{str(event)}'"
            cursor.execute(sql)
            data = cursor.fetchone()
            embed = discord.Embed(
                title=data['name'],
                description=data['description'].replace("\\n","\n"),
                color=discord.Colour.from_rgb(r=255, g=192, b=60)
            )
            user = message.channel.guild.get_member(int(data['host']))
            embed.set_author(name=user.display_name, icon_url=user.avatar_url)
            if "image" in data and data['image'] != "":
                embed.set_image(url=data['image'])
            embed.add_field(name="Date", value=data["date"])
            #embed.add_field(name="Map", value=data["map"])
            embed.set_footer(text="Mission ID: "+str(event))
            sql = f"SELECT * FROM `squads` WHERE `event` = '{str(event)}'"
            cursor.execute(sql)
            squads = cursor.fetchall()
            slot_sql = f"SELECT * FROM `slots` WHERE `event` = '{str(event)}' AND `squad` = '{{}}'"
            for squad in squads:
                slotss = ""
                cursor.execute(slot_sql.format(squad['id']))
                slots = cursor.fetchall()
                for slot in slots:
                    slotss += slot['name'] + ": "
                    if "playerid" in slot and slot['playerid'] != None:
                        slotss += "<@"+str(slot['playerid'])+">\n"
                    else:
                        slotss += "\n"
                embed.add_field(name=squad["name"], value=slotss, inline=False)
            await target.edit(embed=embed, content=None)
    finally:
        connection.close()
