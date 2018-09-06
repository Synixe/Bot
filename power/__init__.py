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
        async with message.channel.typing():
            for dev in Discover.discover().values():
                info = dev.get_sysinfo()
                logger.debug(f"Found device with id: {info['deviceID']} ({info['alias']})")
                if info['deviceId'] == "8006F8AF3EDB4523AE048863748E0BAB1873E878":
                    embed = discord.Embed(
                        title="Primary Server (Ludwig)",
                        color=ctx.bot.profile.color
                    )
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
                    prev = monthly[prev]
                    embed.add_field(name="Previous Month", value=f"{prev}kWh (${(prev * COST):,.2f})", inline=False)
                    embed.add_field(name="Current Month", value=f"{current}kWh (${(current * COST):,.2f})")
        await message.channel.send(embed=embed)
