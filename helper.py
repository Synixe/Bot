import discord
import certs

class Commands():
    def register(self, _):

        return {
            "commands" : {
                "function" : self.commands,
                "description" : "See all the commands available to you",
                "roles" : ["@everyone"]
            },
            "card" : {
                "function" : self.card,
                "description" : "Print a user card for yourself or another user",
                "roles" : ["@everyone"]
            }
        }

    async def commands(self, data, client, message):
        text = ""
        for command in client.commands:
            if client.inRoleList(message.channel.guild, message.author.id, client.commands[command]["roles"]):
                text += command+"\n"
                text += "        "+client.commands[command]["description"]+"\n"
        await message.channel.send(text)

    async def card(self, data, client, message):
        if len(data) == 0:
            user = message.author
        else:
            user = message.channel.guild.get_member(client.getIDFromTag(data[0]))
        embed = discord.Embed(
            title = user.name,
            color = user.colour
        )
        embed.add_field(name="Joined on",value=user.joined_at.strftime("%B %d, %Y"))
        embed.set_thumbnail(url=user.avatar_url)
        c = certs.getCerts()
        if str(user.id) in c:
            embed.set_footer(text=", ".join(c[str(user.id)]))
        await message.channel.send(embed=embed)
