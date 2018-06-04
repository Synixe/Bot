import bot
import discord

import valve.source.a2s

class SteamUpdates(bot.Extension):

    @bot.live()
    @bot.task(120)
    async def arma_player_count(ctx):
        """Post player count to topic of #lookingtoplay"""
        channel = discord.utils.find(lambda c: c.name == "lookingtoplay", discord.utils.find(lambda g: g.name == "Synixe", ctx._bot.guilds).channels)
        try:
            with valve.source.a2s.ServerQuerier(("arma.synixe.com", 2303)) as server:
                info = server.info()
                topic = "Arma 3 Server Online with {} People Playing".format(info['player_count'])
        except valve.source.a2s.NoResponseError:
            topic = "Arma 3 Server Offline"
        finally:
            await channel.edit(topic=topic)
