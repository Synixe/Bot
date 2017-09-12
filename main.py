import discord
import sys
import traceback

import tokens

#commands
import certs
import managers
import youtube
import arma3
import helper
import aar

class SynixeBot(discord.Client):
    async def on_ready(self):
        print("="*20)
        print("Connected")
        print('Username: {0.name}\nID: {0.id}'.format(self.user))
        print("="*20)

        self.commands = {}

        self.commands.update(certs.Commands().register(self))
        self.commands.update(managers.Commands().register(self))
        self.commands.update(youtube.Commands().register(self))
        self.commands.update(arma3.Commands().register(self))
        self.commands.update(helper.Commands().register(self))
        self.commands.update(aar.Commands().register(self))

    async def on_message(self, message):
        await self.execute(message)

    async def execute(self, message):
        if message.content.startswith("!"):
            data = message.content.split(" ")
            cmd = data[0][1:]
            args = []
            try:
                args = data[1:]
            except:
                #No args
                pass
            if cmd in self.commands:
                try:
                    if self.inRoleList(message.channel.guild, message.author.id, self.commands[cmd]["roles"]):
                        await self.commands[cmd]["function"](args, self, message)
                    else:
                        await message.channel.send("You are not allowed to use this command.")
                except Exception as e:
                    await message.channel.send('Error on line {}'.format(sys.exc_info()[-1].tb_lineno)+"\n"+str(type(e).__name__)+"\n"+str(e))
                    traceback.print_exc()
            else:
                await message.channel.send("Unknown Command")
        else:
            #Regular message
            pass

    def isManager(self, guild, id):
        for r in guild.get_member(int(id)).roles:
            if r.name.lower() == "manager":
                return True
        return False

    def inRoleList(self, guild, id, roles):
        for r in guild.get_member(int(id)).roles:
            if r.name.lower() in roles:
                return True
        return False

client = SynixeBot()
client.run(tokens.getToken("discord"))
