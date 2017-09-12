import discord

class Commands():
    def register(self, _):

        return {
            "commands" : {
                "function" : self.commands,
                "description" : "See all the commands available to you",
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
