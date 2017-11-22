import discord
import tokens

class ConnectionsBot(discord.Client):
    async def on_ready(self):
        print("Ready")
        for g in client.guilds:
            if g.name.lower() == "synixe":
                user = g.get_member(self.id)
                print(user.display_name)
                profile = await user.profile()
                self.accounts = profile.connected_accounts
                print("Done")
        await self.logout()

client = ConnectionsBot()
client.id = 307524009854107648
client.run(tokens.getToken("discord2"),bot=False)
print(client.accounts)
