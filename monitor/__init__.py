import discord
import bot

class ServerEvents(bot.Extension):
    @bot.event("on_member_join")
    async def member_join(ctx, member):
        """Display a welcome message and give new members the role of New"""
        for channel in member.guild.channels:
            if channel.name == "lobby":
                lobby = channel
            elif channel.name == "info":
                info = channel
            elif channel.name == "repohelp":
                repohelp = channel
        await lobby.send(
            ("<@{}>! Welcome to Synixe! "+
            "Here is some basic info about our group: "+
            "We play at 7pm PST / 10pm EST. "+
            "We have some mods you'll need to download from <#{}>. "+
            "If you have any questions while getting setup "+
            "ask in <#{}>. We do more than just Arma too, use `?topics` "+
            "to see what other games you can subscribe to.").format(member.id, info.id, repohelp.id)
        )
        await member.add_roles(discord.utils.find(lambda m: m.name.lower() == "new", member.guild.roles))

    @bot.event("on_member_remove")
    async def member_remove(ctx, member):
        """Display a message when a member leaves"""
        channel = discord.utils.find(lambda c: c.name == "botevents", member.guild.channels)
        if channel is None: return
        await channel.send(f"Member Left: {member.display_name}#{member.discriminator} <@{member.id}> ({member.id}")

    @bot.event("on_member_update")
    async def member_update(ctx, args):
        before, after = args
        if before.display_name != after.display_name:
            channel = discord.utils.find(lambda c: c.name == "botevents", after.guild.channels)
            if channel is None: return
            embed = discord.Embed(
                title="Nickname Change",
                color=ctx.profile.color
            )
            embed.add_field(name="Previous Name", value=before.display_name)
            embed.add_field(name="New Name", value=after.display_name)
            await channel.send(embed=embed)
