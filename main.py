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
import poll

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
        self.commands.update(poll.Commands().register(self))

    async def on_message(self, message):
        await self.execute(message)

    async def execute(self, message):
        if message.author.id == self.user.id:
            return
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
            if "ts.synixe.com" in message.content:
                await message.channel.send("Please don't post the TeamSpeak Address. Instead an @Active member needs to use `!ts [user]` to send someone the address.")
                await message.delete()
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

    def getIDFromTag(self, text):
        if text.startswith("<@") or text.startswith("<#"):
            return int(text[2:-1])
        else:
            try:
                return int(text)
            except:
                return text

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

    async def on_member_join(self, member):
        g = self.getGuild("synixe")
        c = self.getChannel(g, "lobby")
        i = self.getChannel(g, "info")
        e = self.getChannel(g, "events")
        r = self.getChannel(g, "repohelp")
        await c.send("<@"+str(member.id) + ">! Welcome to Synixe! Here is some basic info about our group: If you check out <#"+str(e.id)+"> you can see our upcoming missions. We play at 7pm PST / 10pm EST. We have some mods you'll need to download from <#"+str(i.id)+">. If you have any questions while getting those setup we're more than happy to help in <#"+str(r.id)+">.")
        await member.add_roles([discord.utils.get(g.roles, name="New")])

    async def on_member_remove(self, member):
        c = self.getChannel(self.getGuild("synixe"), "botevents")
        await c.send("<@"+str(member.id) + "> ("+member.name+"#"+member.discriminator+") is no longer in the server.")

    async def on_member_ban(g, member):
        c = self.getChannel(g, "botevents")
        await c.send("<@"+str(member.id) + "> ("+member.name+"#"+member.discriminator+") has been banned.")

    async def on_member_unban(g, member):
        c = self.getChannel(g, "botevents")
        await c.send("<@"+str(member.id) + "> ("+member.name+"#"+member.discriminator+") has been unbanned.")

    async def on_message_delete(message):
        if not self.inRoleList(message.channel.guild,message.author.id,["manager","moderator","bot"]):
            c = self.getChannel(self.getGuild("synixe"), "botevents")
            c.send("<@"+str(message.author.id) + "> ("+message.author.name+"#"+message.author.discriminator+") Deleted: "+message.content)

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
