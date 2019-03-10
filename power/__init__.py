import datetime
import discord
import bot
import logger

from pyHS100 import Discover

COST = 0.14228

class PowerUsage(bot.Extension):

    @bot.command()
    async def power(ctx, message):
        """Display Power Usage Information"""
        embeds = []
        async with message.channel.typing():
            for dev in Discover.discover().values():
                info = dev.get_sysinfo()
                logger.debug(f"Found device with id: {info['deviceId']} ({info['alias']})")
                if info['deviceId'] == "800672A01A2AD035078A64A1C1F665FB187369C1":
                    embed = discord.Embed(
                        title="Server (Gregor)",
                        color=ctx.bot.profile.color
                    )
                else:
                    continue
                current = dev.get_emeter_realtime()
                embed.add_field(name="Current Usage",
                                value=f"{round(current['current'], 2)}A@{round(current['voltage'], 2)}V ({round(current['power'], 2)}W)")
                monthly = dev.get_emeter_monthly()
                month = int(datetime.datetime.now().strftime("%m"))
                current = monthly[month]
                prev = month - 1
                if prev == 0:
                    prev = 12
                    monthly = dev.get_emeter_monthly(year=int(datetime.datetime.now().strftime("%Y"))-1)
                try:
                    prev = monthly[prev]
                    embed.add_field(name="Previous Month", value=f"{prev}kWh (${(prev * COST):,.2f})", inline=False)
                except KeyError:
                    logger.debug(f"No previous month for {info['alias']}")
                embed.add_field(name="Current Month", value=f"{current}kWh (${(current * COST):,.2f})", inline=False)
                if month in [9,10] and info['alias'] == "Gregor":
                    embed.set_footer(text="This power monitor was reset, and is not accurate for the month of September")
                embeds.append(embed)
        for embed in embeds:
            await message.channel.send(embed=embed)
