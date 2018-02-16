"""Bot Controls"""
import argparse
import sys
import discord
import logger

class BotExtension:
    """Control of the Bot"""
    def __init__(self, bot):
        self.name = "Bot Controls"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def __register__(self):
        return {
            "stop" : {
                "function" : self.stop,
                "roles" : ["code contributer"],
                "alias" : ["quit"]
            }
        }

    async def stop(self, args, message):
        """Stop the Bot"""
        await message.channel.send("Shutting down...")
        sys.exit(0)
