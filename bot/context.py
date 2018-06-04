import copy

class Context:
    def __init__(self, bot, extension, message):
        self.user = bot.user
        self.profile = bot.profile
        self.extension = extension
        self.message = message
        self.loop = bot.loop

        self._bot = bot

    def safe(self):
        safe = copy.copy(self)
        self._bot = None
        del self._bot
        return safe
