import argparse
import discord
import random
import tokens
import pymysql.cursors

from . import embeds

class BotExtension:
    def __init__(self, bot):
        self.name = "Mini Commands"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def register(self):
        return {
            "slot" : {
                "function" : self.slot,
                "description" : "Slot up for a mission",
                "roles" : ["@everyone"]
            },
            "unslot" : {
                "function" : self.unslot,
                "description" : "Unslot from a mission",
                "roles" : ["@everyone"]
            },
            "post" : {
                "function" : self.post,
                "description" : "Post an event to #events",
                "roles" : ["missionmaker"]
            }
        }

    def getConnection(self):
        return pymysql.connect(
            host = tokens.MYSQL.HOST,
            user = tokens.MYSQL.USER,
            password = tokens.MYSQL.PASS,
            db = tokens.MYSQL.DATA,
            cursorclass = pymysql.cursors.DictCursor
        )

    async def slot(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Slot up for a mission", message))
        parser.add_argument("slot",nargs="*",help=self.bot.processOutput("Slot to take", message))
        parser.add_argument("-m","--mission",nargs="*",help=self.bot.processOutput("Mission to slot into", message))
        args = parser.parse_args(args)
        args.slot = " ".join(args.slot)
        if args.mission != None:
            if ";" in args.slot or ";" in args.mission:
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
                        if m.embeds[0].footer.text.startswith("Mission ID:"):
                            event_id = int(m.embeds[0].footer.text.split(": ")[1])
                            target = m
                    else:
                        if m.embeds[0].title.lower() == args.mission.lower():
                            event_id = int(m.embeds[0].footer.text.split(": ")[1])
                            target = m
            if target != None:
                connection = self.getConnection()
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
                            await embeds.displayEvent(self, target, event_id, message)
                            await message.channel.send(self.bot.processOutput("Slotted into {0} for {1}!".format(slot['name'],target.embeds[0].title), message))
                        else:
                            await message.channel.send(self.bot.processOutput("That role was not found for {}.".format(target.embeds[0].title), message))
                finally:
                    connection.close()

    async def unslot(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Slot up for a mission", message))
        parser.add_argument("-m","--mission",nargs="*",help=self.bot.processOutput("Mission to slot into", message))
        args = parser.parse_args(args)
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
                        if m.embeds[0].footer.text.startswith("Mission ID:"):
                            event_id = int(m.embeds[0].footer.text.split(": ")[1])
                            target = m
                    else:
                        if m.embeds[0].title.lower() == args.mission.lower():
                            event_id = int(m.embeds[0].footer.text.split(": ")[1])
                            target = m
            if target != None:
                connection = self.getConnection()
                try:
                    with connection.cursor() as cursor:
                        sql = "UPDATE `slots` SET `playerid` = NULL WHERE `playerid` = '"+str(message.author.id)+"'"
                        cursor.execute(sql)
                        connection.commit()
                        await message.channel.send(self.bot.processOutput("Unslotted", message))
                        await embeds.displayEvent(self, target, event_id, message)
                finally:
                    connection.close()

    async def post(self, args, message):
        parser = argparse.ArgumentParser(description=self.bot.processOutput("Post an event to #events", message))
        parser.add_argument("event",type=int,help=self.bot.processOutput("ID of the mission to post", message))
        args = parser.parse_args(args)
        channel = discord.utils.find(lambda c: c.name == "events", message.channel.guild.channels)
        if channel is not None:
            mid = await channel.send("Loading Data")
            await embeds.displayEvent(self, mid, args.event, message)
