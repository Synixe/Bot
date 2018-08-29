import bot
import discord

class Topics(bot.Extension):
    """Gaming Topics for Synixe"""

    @bot.argument("topic", str)
    @bot.command()
    async def sub(ctx, message):
        """Subscribe to a topic"""
        categories = message.guild.by_category()
        for category in categories:
            if category[0] != None and category[0].name == "🎮 Gaming":
                for topic in category[1]:
                    if isinstance(topic, discord.TextChannel):
                        if ctx.args.topic.lower() == topic.topic.split(" - ")[0].lower():
                            role = discord.utils.find(
                                lambda r: r.name == topic.topic.split(" - ")[1],
                                message.guild.roles
                            )
                            await message.author.add_roles(role)
                            await topic.send("<@{}> has just subscribed!".format(message.author.id))
                            await message.add_reaction("✅")
                            return

    @bot.command()
    async def topics(ctx, message):
        categories = message.guild.by_category()
        text = ""
        for category in categories:
            if category[0] != None and category[0].name == "🎮 Gaming":
                for topic in category[1]:
                    if isinstance(topic, discord.TextChannel):
                        text += "{}: `{}sub {}`\n".format(
                            topic.topic.split(" - ")[1], ctx.profile.prefix, topic.topic.split(" - ")[0]
                        )
        await message.channel.send(text)
