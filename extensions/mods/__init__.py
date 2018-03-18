"""Arma 3 Mods for Synixe"""
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
        logger.error("Mod Updates will be inactive as it requires pymysql")
        PYMYSQL = False

import asyncio
import discord
import tokens

from . import armaholic
from . import github

class BotExtension:
    """Arma 3 Mods for Synixe"""
    def __init__(self, bot):
        self.name = "Mod Updates"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot
        self.active = PYMYSQL
        self.disable_during_test = True

    def __loops__(self):
        return {
            "mod-update-check" : self.bot.loop.create_task(self.mod_task())
        }

    async def mod_task(self):
        """Checks for mod updates"""
        await self.bot.wait_until_ready()
        channel = discord.utils.find(
            lambda c: c.name == "botevents",
            discord.utils.find(
                lambda g: g.name == "Synixe",
                self.bot.guilds
            ).channels
        )
        if channel != None:
            while not self.bot.is_closed():
                connection = pymysql.connect(
                    host=tokens.MYSQL.HOST,
                    user=tokens.MYSQL.USER,
                    password=tokens.MYSQL.PASS,
                    db=tokens.MYSQL.DATA,
                    cursorclass=pymysql.cursors.DictCursor
                )
                try:
                    with connection.cursor() as cursor:
                        sql = "SELECT * FROM `mods`"
                        cursor.execute(sql)
                        mods = cursor.fetchall()
                        for mod in mods:
                            asyncio.sleep(60)
                            if mod["url"] == "N":
                                continue
                            service, mid = mod['url'].split("@")
                            if service == "A": #Armaholic
                                latest = armaholic.latest(mid)
                                url="http://www.armaholic.com/page.php?id="+mid
                            elif service == "G": #GitHub
                                try:
                                    latest = github.latest(mid)
                                except Exception as e:
                                    continue
                                url = "http://github.com/"+mid

                            if latest != mod['notified']:
                                embed = discord.Embed(
                                    title=mod['name'],
                                    url=url
                                )
                                embed.add_field(name="Current", value=mod['version'])
                                embed.add_field(name="Available", value=latest)
                                await channel.send(embed=embed)
                                sql = "UPDATE `mods` SET `notified` = %s WHERE `id` = %s"
                                cursor.execute(sql, (latest, mod['id']))
                                connection.commit()
                                logger.info("Published update for "+mod['name'])
                finally:
                    connection.close()
                await asyncio.sleep(60 * 60)
