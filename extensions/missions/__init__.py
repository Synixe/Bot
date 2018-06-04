import bot
import discord
from neo4j.v1 import GraphDatabase

class Slotting(bot.Extension):
    """Provides commands for Slotting"""

    @bot.argument("slot", str)
    @bot.command()
    async def slot(ctx, message):
        """Slot into a role for a mission"""
        await message.channel.send("Ya yeet 👎")

class MissionMakers(bot.Extension):
    """Provides commands for MissionMakers"""
