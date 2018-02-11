import client
import tokens
import logger
import argparse
import signal
import sys

parser = argparse.ArgumentParser(description="The Synixe Discord Bot")
parser.add_argument("--debug",action="store_true",help="Enable Debugging")
args = parser.parse_args()

def handler(signal, frame):
    bot.close()
    logger.info("Bot Stopped")
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

logger.clear()
logger.set_debug(args.debug)

bot = client.BotClient()
logger.info("Starting Bot")
bot.run(tokens.DISCORD)
