import discord
import pymysql.cursors
import tokens

class BotExtension:
    def __init__(self, bot):
        self.name = "Mod Updates"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def loops(self):
        return {
            "mod-update-check" : self.bot.loop.create_task(self.mod_task())
        }

    async def mod_task(self):
        print("Mod Task")
        await self.bot.wait_until_ready()
        connection = pymysql.connect(
            host = tokens.MYSQL.HOST,
            user = tokens.MYSQL.USER,
            password = tokens.MYSQL.PASS,
            db = token.MYSQL.DATA,
            cursorclass = pymysql.cursors.DictCursor
        )
        while not client.is_closed():
            print("Mod Loop")
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `mods`"
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    print(result)
            finally:
                connection.close()
