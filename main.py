import client
import tokens
import logger

logger.clear()

bot = client.BotClient()
bot.prefix = "?"
bot.run(tokens.DISCORD, bot=False)
