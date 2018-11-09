import bot
import discord

import random
import logger

class Twitch(bot.Extension):
    """Twitch Features"""

    @bot.event("on_member_update")
    async def streaming_notification(ctx, args):
        """Posts to #streams if a user starts streaming"""
        before, after = args
        if ctx.in_role_list(after, ["active"]):
            channel = discord.utils.find(lambda c: c.name == "streams", after.guild.channels)
            logger.debug(f"Channel {channel}")
            if channel != None:
                if after.activity != None and isinstance(after.activity, discord.Streaming):
                    if before.activity == None or not isinstance(before.activity, discord.Streaming):
                        taglines = [
                            "Grab some popcorn, {} is streaming!",
                            "Lights, Camera, Action! {} is streaming!",
                            "{} is now live!",
                            "Sit back and relax. {} is now streaming!",
                            "{} enters from stage left and is now streaming!",
                            "{} just went live!",
                            "Feel like stream sniping? {} just went live!",
                            "Hope they survive. {} just went live!",
                            "Ready to revive? {} is now live!",
                            "Stop that daydream! Watch {}'s Stream!",
                            "Is this a glitch? No! {} really is live on Twitch!",
                            "They're ready to aim, {} is streaming a game!",
                            "Ya'll gonna want to check this shit out, {} is streaming!"
                        ]
                        embed = discord.Embed(
                            title=after.activity.name,
                            url=after.activity.url,
                            description=after.activity.details,
                            color=ctx.profile.color
                        )
                        embed.set_author(name=after.display_name)
                        embed.set_thumbnail(url=after.avatar_url)
                        embed.set_footer(text=after.display_name)
                        await channel.send(embed=embed, content=random.choice(taglines).format(after.display_name))
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
