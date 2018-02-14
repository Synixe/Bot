"""Synixe Discord Bot"""
import client
import tokens
import logger
import argparse
import signal
import sys

try:
    from os import environ
    environ['SHELL']
except KeyError:
    logger.error("The Windows CMD is not supported. Please use a shell like Git Bash.")
    sys.exit(1)

class Bot:
    """Shell of the Synixe Bot"""
    @classmethod
    def run(cls):
        """Run the bot"""
        parser = argparse.ArgumentParser(description="The Synixe Discord Bot")
        parser.add_argument("--debug", action="store_true", help="Enable Debugging")
        args = parser.parse_args()

        def handler(signal, frame):
            """Handle a signal"""
            bot.close()
            logger.info("Bot Stopped")
            sys.exit(0)

        signal.signal(signal.SIGINT, handler)

        logger.clear()
        logger.set_debug(args.debug)

        bot = client.BotClient()
        logger.info("Starting Bot")
        bot.run(tokens.DISCORD)

if __name__ == "__main__":
    Bot().run()
