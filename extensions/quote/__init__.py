"""Quotes from database"""
import logger
try:
    import pymysql.cursors
    PYMYSQL = True
except ImportError:
    import dep
    if dep.ask("pymysql"):
        try:
            import pymysql.cursors
            PYMYSQL = True
            logger.info("pymysql Installed!", "green")
        except ImportError:
            logger.error("Failed to install pymysql")
    else:
        logger.error("Quoter will be unavailable as it requires pymysql")
        PYMYSQL = False

import asyncio
import random
import discord
import tokens
import argparse

class BotExtension:
    """Quoter"""
    def __init__(self, bot):
        self.name = "Quote System"
        self.author = "nameless + Brett"
        self.version = "1.0"
        self.bot = bot
        self.active = PYMYSQL
        self.disable_during_test = False

    def __register__(self):
        return {
            "quote" : {
                "function": self.quote,
                "roles" : ["@everyone"]
            },
            "save" : {
                "function" : self.save,
                "roles" : ["active"]
            }
        }

    async def quote(self, args, message):
        """Pulls Quotes from the Database"""
        parser = argparse.ArgumentParser(description=self.quote.__doc__)
        parser.add_argument("user", nargs="?", default="%", help="user to quote") #what is an % meant to be, a wildcard, it will match anything
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            id = str(self.bot.get_from_tag(args.user))
            connection = pymysql.connect(
                host=tokens.MYSQL.HOST,
                user=tokens.MYSQL.USER,
                password=tokens.MYSQL.PASS,
                db=tokens.MYSQL.DATA,
                cursorclass=pymysql.cursors.DictCursor
            )
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `quotes` WHERE `user` LIKE '"+id+"' ORDER BY RAND() LIMIT 1"
                    cursor.execute(sql)
                    quote = cursor.fetchone()
                    if quote != None:
                        user = message.channel.guild.get_member(int(quote["user"]))
                        embed = discord.Embed(
                            color=discord.Colour.from_rgb(r=255, g=192, b=60),
                            description=quote['text']
                        )
                        embed.set_author(name=user.name, icon_url=user.avatar_url)
                        embed.set_footer(text=quote["date"].strftime("%m/%d/%y"))
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("That user doesn't have any quotes")
            finally:
                if connection != None:
                    connection.close()

    async def save(self, args, message):
        """Saving Quotes to the Database"""
        parser = argparse.ArgumentParser(description=self.save.__doc__)
        parser.add_argument("messages", nargs="+", help="messages to save")
        args = await self.bot.parse_args(parser, args, message)
        if args != False:
            connection = pymysql.connect(
                host=tokens.MYSQL.HOST,
                user=tokens.MYSQL.USER,
                password=tokens.MYSQL.PASS,
                db=tokens.MYSQL.DATA,
                cursorclass=pymysql.cursors.DictCursor
            )
            try:
                text = ""
                first = None
                for mid in args.messages:
                    msg = await message.channel.get_message(mid)
                    text += msg.content + "\n"
                    if first == None:
                        first = msg
                    elif first.author != msg.author:
                        await message.channel.send("All messages must have the same author.")
                        return
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `quotes` (`_id`, `text`, `channel`, `user`, `date`) VALUES (NULL, '"+text+"', '"+str(message.channel.id)+"', '"+str(first.author.id)+"', '"+(first.created_at.strftime("%Y-%m-%d"))+"')"
                    cursor.execute(sql)
                connection.commit()
                embed = discord.Embed(
                    color=discord.Colour.from_rgb(r=255, g=192, b=60),
                    description=text
                )
                embed.set_author(name=first.author.name, icon_url=first.author.avatar_url)
                embed.set_footer(text=first.created_at.strftime("%m/%d/%y"))
                await message.channel.send("Saved the following quote to the database:", embed=embed)
            finally:
                if connection != None:
                    connection.close()
