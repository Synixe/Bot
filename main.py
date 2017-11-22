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
import update
import server

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
        self.commands.update(update.Commands().register(self))
        self.commands.update(server.Commands().register(self))

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
            print("Incoming Command:",cmd)
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

    def getChannel(self, guild, channel):
        for c in guild.channels:
            if c.name.lower() == channel:
                return c
        return None

    def getGuild(self, guild):
        for g in client.guilds:
            if guild.lower() in g.name.lower():
                return g
        return None

    async def on_member_remove(self, member):
        c = self.getChannel(self.getGuild("synixe"), "botevents")
        await c.send("<@"+str(member.id) + "> is no longer in the server.")

    async def on_member_update(self, before, after):
        if before.nick == None:
            nickbefore = before.name
        else:
            nickbefore = before.nick
        if after.nick == None:
            nickafter = after.name
        else:
            nickafter = after.nick
        if nickbefore != nickafter:
            c = self.getChannel(self.getGuild("synixe"), "botevents")
            await c.send(nickbefore + " is now known as " + nickafter)

        print(after.game)
        if after.game != None:
            print(after.game.url)
            if after.game.url != None:
                if before.game.url == None:
                    c = self.getChannel(self.getGuild("synixe"), "random")
                    import random
                    lines = open('./data/streaming').read().splitlines()
                    await c.send(random.choice(lines).format(nickafter) + "\n"+ after.game.url)

try:
    client = SynixeBot()
    client.run(tokens.getToken("discord"))
except KeyboardInterrupt:
    print("Shutting Down")
    client.close()
