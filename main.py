import client
import tokens
import logger

logger.clear()

bot = client.BotClient()
print("Starting Bot")
bot.prefix = "?"
bot.run(tokens.DISCORD)
