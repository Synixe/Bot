import bot
import discord

import random

class Twitch(bot.Extension):
    """Twitch Features"""

    @bot.live()
    @bot.event("member_update")
    async def streaming_notification(ctx, before, after):
        """Posts to #streams if a user starts streaming"""
        if ctx.in_role_list(after, ["active"]):
            channel = discord.utils.find(lambda c: c.name == "streams", after.guild.channels)
            if channel != None:
                if after.activity != None and isinstance(after.activity, discord.Streaming):
                    if before.activity == None or not isinstance(before.activity, discord.Streaming):
                        lines = open('./extensions/twitch/taglines.txt').read().splitlines()
                        embed = discord.Embed(
                            title=after.activity.name,
                            url=after.activity.url,
                            description=after.activity.details,
                            color=ctx.profile.color
                        )
                        embed.set_author(name=after.display_name)
                        embed.set_thumbnail(url=after.avatar_url)
                        embed.set_footer(text=after.display_name)
                        await channel.send(embed=embed, content=random.choice(lines).format(after.display_name))
                elif after.activity == None or not isinstance(after.activity, discord.Streaming):
                    if before.activity != None and isinstance(before.activity, discord.Streaming):
                        messages = channel.history(limit=50)
                        target = None
                        async for msg in messages:
                            if len(msg.embeds) == 1:
                                try:
                                    if msg.embeds[0].footer.text == before.display_name:
                                        target = msg
                                except:
                                    pass
                        if target != None:
                            await msg.delete()
