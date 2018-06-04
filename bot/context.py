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

    def in_role_list(member, roles):
        """Check if a member is in a list of roles"""
        if "@everyone" in roles:
            return True
        if isinstance(member, discord.User):
            return False
        for r in member.roles:
            if r.name.lower() in roles:
                return True
        return False
