"""Time commands"""
import argparse
import random
import discord
import datetime
import logger
try:
    import pytz
    PYTZ = True
except ImportError:
    import dep
    if dep.ask("pytz"):
        try:
            import pytz
            PYTZ = True
            logger.info("pytz Installed!", "green")
        except ImportError:
            logger.error("Failed to install pytz")
    else:
        logger.error("time will be inactive as it requires pytz")
        PYTZ = False

class BotExtension:
    """Time Commands"""
    def __init__(self, bot):
        self.name = "Time Commands"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

    def __register__(self):
        return {
            "time" : {
                "function" : self.time,
                "roles" : ["@everyone"]
            }
        }

    async def time(self, args, message):
        """Prints out the time in different timezones"""
        if PYTZ:
            parser = argparse.ArgumentParser(description=self.time.__doc__)
            parser.add_argument("offset", help="An offset in 4 digit format from STC")
            parser.add_argument("timezone", nargs="?", help="A specific timezone to display")
            args = await self.bot.parse_args(parser, args, message)
            if args != False:
                negative = False
                if args.offset.startswith("-"):
                    negative = True
                    args.offset = args.offset[1:]
                if len(args.offset) != 4:
                    await message.channel.send("Offset must be in 4 digit format. Example: -0100 for 1 hour before STC")
                    return
                day = datetime.datetime.now(tz=pytz.timezone("America/New_York"))
                stc = pytz.timezone("America/New_York").localize(datetime.datetime(day.year, day.month, day.day, 22, 0, 0))

                if negative:
                    stc -= datetime.timedelta(hours=int(args.offset[0:2]), minutes=int(args.offset[2:4]))
                else:
                    stc += datetime.timedelta(hours=int(args.offset[0:2]), minutes=int(args.offset[2:4]))

                west = stc.astimezone(pytz.timezone("US/Pacific"))
                east = stc
                ausi = stc.astimezone(pytz.timezone("Australia/Sydney"))

                if args.timezone:
                    if args.timezone in pytz.all_timezones:
                        special = stc.astimezone(pytz.timezone(args.timezone))
                else:
                    special = None

                strfmt = "%A **%I:%M** %p %Z"
                m = "Western: {}\nEastern: {}\nSydney: {}\n".format(
                    west.strftime(strfmt),
                    east.strftime(strfmt),
                    ausi.strftime(strfmt))

                if special != None:
                    m += "\n{}: {}".format(args.timezone, special.strftime(strfmt))

                await message.channel.send(m)
