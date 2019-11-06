"""Teamspeak for Disco"""
import discord
import bot

class Swifty(bot.Extension):
    @bot.event("on_message")
    async def swifty_error(ctx, message):
        """Swifty Error Responder"""
        if "System.Net.WebException: The request was aborted: Could not create SSL/TLS secure channel.".lower() in message.content.lower():
            await message.channel.send("Due to Swifty refusing to acknowledge that bug exists, HTTPS has been disabled. Please change your repo address to `http://repo.synixe.com`")
        elif "A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond 69.11.99.171:443".lower() in message.content.lower():
            await message.channel.send("Due to Swifty refusing to acknowledge that bug exists, HTTPS has been disabled. Please change your repo address to `http://repo.synixe.com`")
        elif "System.IO.IOException: There is not enough space on the disk.".lower() in message.content.lower():
            await message.channel.send("The disk with your mod folder is full, move the mod folder to another disk immediately and change the path. http://repo.synixe.com/swifty3.png")
        elif "System.Exception: Could not locate 'arma3launcher.exe'".lower() in message.content.lower():
            await message.channel.send("The Arma 3 Directory in your settings is not correct, point it to the Arma 3 Directory in your `steamapps/common`.")
        elif "System.Exception: Steam is not running, Start Steam and try again".lower() in message.content.lower():
            await message.channel.send("> Steam is not running, Start Steam and try again")
        elif "System.IO.IOException: Unable to read data from the transport connection".lower() in message.content.lower():
            await message.channel.send("You lost your internet connection while Swifty was downloading mods, your computer may have went to sleep")
