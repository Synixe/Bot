"""Slotting For Mission Sheets"""
import argparse
import logger
try:
    import pymysql.cursors
    PYMYSQL = True
except ImportError:
    import dep
    if dep.ask("pymysql"):
        try:
            import pymysql.cursors
            PYMYSQL = True
            logger.info("pymysql Installed!", "green")
        except ImportError:
            logger.error("Failed to install pymysql")
    else:
        logger.error("Slotting will be inactive as it requires pymysql")
        PYMYSQL = False

import datetime
import asyncio
import discord
import tokens

from . import embeds

class BotExtension:
    """Slotting For Mission Sheets"""
    def __init__(self, bot):
        self.name = "Slotting"
        self.author = "Brett + nameless"
        self.version = "1.1"
        self.bot = bot
        self.active = PYMYSQL
        self.disable_during_test = True

    def __register__(self):
        return {
            "slot" : {
                "function" : self.slot,
                "roles" : ["@everyone"]
            },
            "unslot" : {
                "function" : self.unslot,
                "roles" : ["@everyone"]
            },
            "post" : {
                "function" : self.post,
                "roles" : ["missionmaker"]
            }
        }

    def __loops__(self):
        return {
            "schedule-update-check" : self.bot.loop.create_task(self.schedule_task())
        }

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

    async def slot(self, args, message):
        """Slot up for a mission"""
        parser = argparse.ArgumentParser(description=self.slot.__doc__)
        parser.add_argument("slot", nargs="*", help="Slot to take")
        parser.add_argument("-m", "--mission", nargs="*", help="Mission to slot into")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            args.slot = " ".join(args.slot)
            if ";" in args.slot or (args.mission != None and ";" in args.mission):
                await message.channel.send(":laughing:")
                return
            if args.mission != None:
                args.mission = " ".join(args.mission)
            channel = discord.utils.find(lambda c: c.name == "events", message.channel.guild.channels)
            if channel is not None:
                event_id = 0
                target = None
                messages = channel.history(limit=10)
                async for msg in messages:
                    if len(msg.embeds) == 1:
                        if args.mission == None:
                            try:
                                if msg.embeds[0].footer.text.startswith("Mission ID:"):
                                    event_id = int(msg.embeds[0].footer.text.split(": ")[1])
                                    target = msg
                            except AttributeError:
                                pass
                        else:
                            if msg.embeds[0].title.lower() == args.mission.lower() or msg.embeds[0].title.lower().replace("operation ","") == args.mission.lower():
                                event_id = int(msg.embeds[0].footer.text.split(": ")[1])
                                target = msg
                if target != None:
                    connection = self.get_connection()
                    try:
                        with connection.cursor() as cursor:
                            sql = "SELECT * FROM `slots` WHERE (`event` = "+str(event_id)+") AND (LOWER(`name`) LIKE '%"+args.slot.lower()+"%') AND (`playerid` IS NULL)"
                            cursor.execute(sql)
                            data = cursor.fetchall()
                            if len(data) != 0:
                                slot = data[0]
                                sql = "UPDATE `slots` SET `playerid` = NULL WHERE `playerid` = '"+str(message.author.id)+"'"
                                cursor.execute(sql)
                                sql = "UPDATE `slots` SET `playerid` = '"+str(message.author.id)+"' WHERE `id` = '"+str(slot['id'])+"'"
                                cursor.execute(sql)
                                connection.commit()
                                await embeds.display_event(self, target, event_id, message)
                                await message.channel.send("Slotted into {0} for {1}!".format(slot['name'], target.embeds[0].title))
                            else:
                                await message.channel.send("That role was not found for {}.".format(target.embeds[0].title))
                    finally:
                        connection.close()
                else:
                    if args.mission == None:
                        await message.channel.send("No mission is posted!")
                    else:
                        await message.channel.send("That mission doesn't exist!")

    async def unslot(self, args, message):
        """Unslot from a mission"""
        parser = argparse.ArgumentParser(description=self.unslot.__doc__)
        parser.add_argument("-m", "--mission", nargs="*", help="Mission to slot into")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            if args.mission != None:
                if ";" in args.mission:
                    await message.channel.send(":laughing:")
                    return
            if args.mission != None:
                args.mission = " ".join(args.mission)
            channel = discord.utils.find(lambda c: c.name == "events", message.channel.guild.channels)
            if channel is not None:
                event_id = 0
                target = None
                messages = channel.history(limit=10)
                async for m in messages:
                    if len(m.embeds) == 1:
                        if args.mission == None:
                            try:
                                if m.embeds[0].footer.text.startswith("Mission ID:"):
                                    event_id = int(m.embeds[0].footer.text.split(": ")[1])
                                    target = m
                            except AttributeError:
                                pass
                        else:
                            if m.embeds[0].title.lower() == args.mission.lower() or m.embeds[0].title.lower().replace("operation ","") == args.mission.lower():
                                event_id = int(m.embeds[0].footer.text.split(": ")[1])
                                target = m
                if target != None:
                    connection = self.get_connection()
                    try:
                        with connection.cursor() as cursor:
                            sql = "UPDATE `slots` SET `playerid` = NULL WHERE `playerid` = '"+str(message.author.id)+"'"
                            cursor.execute(sql)
                            connection.commit()
                            await message.channel.send("Unslotted from {}".format(target.embeds[0].title))
                            await embeds.display_event(self, target, event_id, message)
                    finally:
                        connection.close()
                else:
                    if args.mission == None:
                        await message.channel.send("No mission is posted!")
                    else:
                        await message.channel.send("That mission doesn't exist!")

    async def post(self, args, message):
        """Post an event to #events"""
        parser = argparse.ArgumentParser(description=self.post.__doc__)
        parser.add_argument("event", type=int, help="ID of the mission to post")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            channel = discord.utils.find(lambda c: c.name == "events", message.channel.guild.channels)
            if channel is not None:
                mid = await channel.send("Loading Data")
                await embeds.display_event(self, mid, args.event, message)

    async def schedule_task(self):
        """Checks for changes to the schedule and posts them in #events"""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            channel = discord.utils.find(lambda c: c.name == "events", discord.utils.find(lambda g: g.name == "Synixe", self.bot.guilds).channels)
            target = None
            if channel is not None:
                messages = channel.history(limit=10)
                async for msg in messages:
                    if len(msg.embeds) == 1:
                        if msg.embeds[0].title == "Upcoming Events":
                            target = msg
            connection = pymysql.connect(
                host=tokens.MYSQL.HOST,
                user=tokens.MYSQL.USER,
                password=tokens.MYSQL.PASS,
                db=tokens.MYSQL.DATA,
                cursorclass=pymysql.cursors.DictCursor
            )
            try:
                now = datetime.datetime.now()
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `events` ORDER BY date ASC"
                    cursor.execute(sql)
                    events = cursor.fetchall()
                    embed = discord.Embed(
                        title="Upcoming Events",
                        color=discord.Colour.from_rgb(r=255, g=192, b=60),
                        description="Sunday Missions: 2pm PST / 5pm EST / 9am Monday AEDT\nAll other Missions: 7pm PST / 10pm EST / 2pm AEDT\nUnless stated otherwise\n\n"
                    )
                    for event in events:
                        date = [x.replace(",", "") for x in event['date'].strip().split(" ")]
                        month, day, year = tuple(date)
                        day = int(day)
                        year = int(year)
                        month = datetime.datetime.strptime(month, '%B').month
                        if month < now.month or (month == now.month and day < now.day):
                            continue
                        if month > now.month and now.day < 15:
                            continue
                        embed.add_field(name=event["date"], value="{} by <@{}>".format(event["name"], event['host']), inline=False)

                    if target == None:
                        await channel.send(embed=embed)
                    else:
                        await target.edit(embed=embed)
            finally:
                connection.close()
            await asyncio.sleep(60 * 60)
