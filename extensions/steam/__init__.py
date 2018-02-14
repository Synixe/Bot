"""Steam Server API"""
import argparse
import asyncio
import discord
import logger
try:
    import valve.source.a2s
    PYVALVE = True
except ImportError:
    import dep
    if dep.ask("python-valve"):
        try:
            import valve.source.a2s
            PYMYSQL = True
            logger.info("pymysql Installed!", "green")
        except ImportError:
            logger.error("Failed to install python-valve")
    else:
        logger.error("Steam Server Monitor will be inactive as it requires python-valve")
        PYVALVE = False

class BotExtension:
    """This handles steam API for the bot"""
    def __init__(self, bot):
        self.name = "Steam Server Monitor"
        self.author = "nameless + Brett"
        self.version = "1.0"
        self.bot = bot
        self.active = PYVALVE
        self.disable_during_test = True

    def __loops__(self):
        return {
            "server-update" : self.bot.loop.create_task(self.server_task())
        }

    async def server_task(self):
        """Post player count to topic of #lookingtoplay"""
        await self.bot.wait_until_ready()
        channel = discord.utils.find(lambda c: c.name == "lookingtoplay", discord.utils.find(lambda g: g.name == "Synixe", self.bot.guilds).channels)
        while not self.bot.is_closed():
            try:
                with valve.source.a2s.ServerQuerier(("arma.synixe.com", 2303)) as server:
                    info = server.info()
                    topic = "ArmA Server Online with {} People Playing".format(info['player_count'])
            except valve.source.a2s.NoResponseError:
                topic = "ArmA Server Offline"
            finally:
                await channel.edit(topic=topic)
                await asyncio.sleep(60 * 2)
