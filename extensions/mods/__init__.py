import discord
import pymysql.cursors
import tokens
import logger
import asyncio

from . import armaholic
from . import github

class BotExtension:
    def __init__(self, bot):
        self.name = "Mod Updates"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def loops(self):
        return {
            "mod-update-check" : self.bot.loop.create_task(self.mod_task())
        }

    async def mod_task(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            connection = pymysql.connect(
                host = tokens.MYSQL.HOST,
                user = tokens.MYSQL.USER,
                password = tokens.MYSQL.PASS,
                db = tokens.MYSQL.DATA,
                cursorclass = pymysql.cursors.DictCursor
            )
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `mods`"
                    cursor.execute(sql)
                    mods = cursor.fetchall()
                    for m in mods:
                        if m["url"] == "N":
                            continue
                        service,mid = m['url'].split("@")
                        if service == "A": #Armaholic
                            latest = armaholic.latest(mid)
                            if latest != m['notified']:
                                for guild in self.bot.guilds:
                                    channel = discord.utils.find(lambda c: c.name == "botevents", guild.channels)
                                    if channel is not None:
                                        embed = discord.Embed(
                                            title = m['name'],
                                            url = "http://www.armaholic.com/page.php?id="+mid
                                        )
                                        embed.add_field(name="Current", value=m['version'])
                                        embed.add_field(name="Available", value=latest)
                                        await channel.send(embed=embed)
                                        sql = "UPDATE `mods` SET `notified` = %s WHERE `id` = %s"
                                        cursor.execute(sql,(latest, m['id']))
                                        connection.commit()
                                        logger.info("Published update for "+m['name'])
                                    else:
                                        frame = getframeinfo(currentframe())
                                        logger.throw("Unable to find #botevents\n\t{0.filename} line {0.lineno - 4}".format(frame))
                            elif service == "G": #GitHub
                                latest = github.latest(mid)
                                if latest != m['notified']:
                                    for guild in self.bot.guilds:
                                        channel = discord.utils.find(lambda c: c.name == "botevents", guild.channels)
                                        if channel is not None:
                                            emded = discord.Embed(
                                                title = m['name'],
                                                url = "http://github.com/"+mid
                                            )
                                            embed.add_field(name="Current", value=m['version'])
                                            embed.add_field(name="Available", value=latest)
                                            await channel.send(embed=embed)
                                            sql = "UPDATE `mods` SET `notified` = %s WHERE `id` = %s"
                                            cursor.execute(sql, (latest, m['id']))
                                            connect.commit()
                                            logger.info("Published update for "+m['name'])
                                        else:
                                            frame = getframeinfo(currentframe())
                                            logger.throw("Unable to find #botevents\n\t{0.filename} line {0.lineno - 4}".format(frame))
            finally:
                connection.close()
            await asyncio.sleep(60 * 60)
