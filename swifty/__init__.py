"""Teamspeak for Disco"""
import discord
import bot

class Swifty(bot.Extension):
    @bot.event("on_message")
    async def swifty_error(ctx, message):
        """Swifty Error Responder"""
        if "System.Net.WebException: The request was aborted: Could not create SSL/TLS secure channel.".lower() in message.content.lower():
            await message.channel.send("Due to Swifty refusing to acknowledge that bug exists, HTTPS has been disabled. Please change your repo address to `http://repo.synixe.com`")
        elif "System.IO.IOException: There is not enough space on the disk.".lower() in message.content.lower():
            await message.channel.send("The disk with your mod folder is full, move the mod folder to another disk immediately and change the path. http://repo.synixe.com/swifty3.png")
        elif "System.Exception: Could not locate 'arma3launcher.exe'".lower() in message.content.lower():
            await message.channel.send("The Arma 3 Directory in your settings is not correct, point it to the Arma 3 Directory in your `steamapps/common`.")
