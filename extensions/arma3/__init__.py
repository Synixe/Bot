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

import urllib.request
import re
import asyncio
import discord
import tokens

class BotExtension:
    """Arma 3 Mods for Synixe"""
    def __init__(self, bot):
        self.name = "Arma 3 Updates"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot
        self.active = PYMYSQL
        self.disable_during_test = False

    def __loops__(self):
        return {
            "arma-update-check" : self.bot.loop.create_task(self.arma_task())
        }

    async def arma_task(self):
        """Checks for Arma 3 updates"""
        regex = r"branch=public\">?\s+<b>public<\/b>?\s+<\/a>?\s+<\/td>?\s+<td><\/td>?\s+<td class=\"b\">?\s+<a href=\"\/patchnotes\/([0-9]+?)\/\">"
        await self.bot.wait_until_ready()
        channel = discord.utils.find(
            lambda c: c.name == "general",
            discord.utils.find(
                lambda g: g.name == "Synixe",
                self.bot.guilds
            ).channels
        )
        if channel != None:
            while not self.bot.is_closed():
                req = urllib.request.Request(url="https://steamdb.info/app/107410/depots/", headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
                with urllib.request.urlopen(req) as response:
                    data = response.read().decode("UTF-8").split("Branches",1)[1].split("</tbody>",1)[0]
                current = re.search(regex, data).group(1)
                connection = pymysql.connect(
                    host=tokens.MYSQL.HOST,
                    user=tokens.MYSQL.USER,
                    password=tokens.MYSQL.PASS,
                    db=tokens.MYSQL.DATA,
                    cursorclass=pymysql.cursors.DictCursor
                )
                try:
                    with connection.cursor() as cursor:
                        sql = "SELECT build FROM `arma` ORDER BY `id` DESC LIMIT 1"
                        cursor.execute(sql)
                        previous = cursor.fetchone()['build']
                        if current != previous:
                            sql = "INSERT INTO `arma` (`build`) VALUES ('"+current+"')"
                            cursor.execute(sql)
                            connection.commit()
                            embed = discord.Embed(
                                title="ArmA 3 Build Updated",
                                url="https://dev.arma3.com/spotrep"
                            )
                            await channel.send(embed=embed)
                finally:
                    connection.close()
                await asyncio.sleep(60 * 60)
