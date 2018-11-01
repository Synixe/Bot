import pymongo
import discord
import bot
import urllib.request

class Slotting(bot.Extension):
    """Provides commands for Slotting"""

    @bot.argument("role+", str)
    @bot.command()
    async def slot(ctx, message):
        """Slot into a role for a mission"""
        if ";" in ctx.args.role:
            return
        channel = discord.utils.find(lambda c: c.name == "events", message.channel.guild.channels)
        if channel is not None:
            event_id = 0
            target = None
            messages = channel.history(limit=10)
            async for msg in messages:
                if len(msg.embeds) == 1:
                    try:
                        event_id = msg.embeds[0].footer.text
                        target = msg
                    except AttributeError:
                        pass
            if target != None:
                dbclient = pymongo.MongoClient("mongodb://192.168.1.81:27017/")
                db = dbclient["dynulo-client"]
                col = db["events"]

                event = col.find({"id": event_id})[0]

                good = False

                for squad in event['squads']:
                    counter = 1
                    for slot in squad['slots']:
                        if not good and ctx.args.role.lower() in slot['name'].lower() or ctx.args.role.lower() in squad['name'].lower()+"-"+str(counter):
                            if "player" not in slot or slot['player'] == None:
                                slot['player'] = str(message.author.id)
                                await message.add_reaction("✅")
                                good = True
                        else:
                            if "player" in slot and str(slot["player"]) == str(message.author.id):
                                del slot["player"]
                        counter += 1
                if not good:
                    await message.add_reaction("👎")
                else:
                    col.update_one({"id": event_id}, {"$set": {"squads": event['squads']}})
                    urllib.request.urlopen("http://192.168.1.81:4200/api/events/update/?id="+event_id+"&msg="+str(target.id)).read()
