"""Timezone checker for Disco"""
import random
import datetime
import discord
import pytz
import bot

class TimeZone(bot.Extension):
    """Timezone checker for Disco"""

    @bot.argument("[offset]")
    @bot.argument("[timezone]")
    @bot.command()
    async def time(ctx, message):
        """Displays a list of different timezones"""
        negative = False
        if ctx.args.offset.startswith("-"):
            negative = True
            ctx.args.offset = ctx.args.offset[1:]
        if len(ctx.args.offset) != 4:
            await message.channel.send("Offset must be in 4 digit format. Example: -0100 for 1 hour before STC")
            return
        day = datetime.datetime.now(tz=pytz.timezone("America/New_York"))
        stc = pytz.timezone("America/New_York").localize(datetime.datetime(day.year, day.month, day.day, 22, 0, 0))

        if negative:
            stc -= datetime.timedelta(hours=int(ctx.args.offset[0:2]), minutes=int(ctx.args.offset[2:4]))
        else:
            stc += datetime.timedelta(hours=int(ctx.args.offset[0:2]), minutes=int(ctx.args.offset[2:4]))

        west = stc.astimezone(pytz.timezone("US/Pacific"))
        east = stc
        ausi = stc.astimezone(pytz.timezone("Australia/Sydney"))

        special = None
        if ctx.args.timezone:
            if ctx.args.timezone in pytz.all_timezones:
                special = stc.astimezone(pytz.timezone(ctx.args.timezone))
            else:
                await message.channel.send("That timezone couldn't be found")

        strfmt = "%A **%I:%M** %p %Z"
        m = "Western: {}\nEastern: {}\nSydney: {}\n".format(
            west.strftime(strfmt),
            east.strftime(strfmt),
            ausi.strftime(strfmt))

        if special != None:
            m += "\n{}: {}".format(ctx.args.timezone, special.strftime(strfmt))

        await message.channel.send(m)
