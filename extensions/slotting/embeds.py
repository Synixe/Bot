"""Embed Creator for Event Sheets"""
import discord

async def display_event(extension, target, event, message):
    """Display an event sheet in #events"""
    connection = extension.getConnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `events` WHERE `id` = '" + str(event) + "'"
            cursor.execute(sql)
            data = cursor.fetchone()
            embed = discord.Embed(
                title=data['name'],
                description=data['description'].replace("\\n","\n"),
                color=discord.Colour.from_rgb(r=255, g=192, b=60)
            )
            user = message.channel.guild.get_member(extension.bot.get_from_tag(str(data['host'])))
            embed.set_author(name=user.display_name, icon_url=user.avatar_url)
            if "image" in data and data['image'] != "":
                embed.set_image(url=data['image'])
            embed.add_field(name="Date", value=data["date"])
            embed.add_field(name="Map", value=data["map"])
            embed.set_footer(text="Mission ID: "+str(event))
            sql = "SELECT * FROM `squads` WHERE `event` = '"+str(event)+"'"
            cursor.execute(sql)
            squads = cursor.fetchall()
            slot_sql = "SELECT * FROM `slots` WHERE `event` = '"+str(event)+"' AND `squad` = '{}'"
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
