import client
import tokens
import logger

logger.clear()

bot = client.BotClient()
logger.info("Starting Bot")
bot.prefix = "?"
bot.run(tokens.DISCORD)
