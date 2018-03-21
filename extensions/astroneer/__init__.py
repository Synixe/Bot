"""Astroneer Wiki"""
import argparse
import urllib.request
import discord
import re

class BotExtension:
    """Astroneer Wiki"""
    def __init__(self, bot):
        self.name = "Astroneer Wiki"
        self.author = "Brett"
        self.version = "1.0"
        self.bot = bot

        self.field_regex = r"<th>\s?(.+?)\s?</th>\s?<td>\s?(.+?)\s?</td></tr>"
        self.image_regex = r"src=\"(.+?)\""
        self.name_regex = r"<th colspan=\"2\" class=\"infoboxname\">\s?(.+?)\s?</th>"
        self.title_regex = r"<h1 id=\"firstHeading\".+?>(.+?)</h1>"

    def __register__(self):
        return {
            "astro" : {
                "function" : self.astro,
                "roles" : ["@everyone"]
            }
        }

    async def astro(self, args, message):
        """Get information from the Astroneer Wiki"""
        async with message.channel.typing():
            parser = argparse.ArgumentParser(description=self.astro.__doc__)
            parser.add_argument("object", help="Object to search for")
            args = await self.bot.parse_args(parser, args, message)
            if args != False:
                try:
                    req = urllib.request.Request(url="https://astroneer.gamepedia.com/"+args.object, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
                    with urllib.request.urlopen(req) as response:
                        data = response.read().decode("UTF-8")
                        try:
                            data = data.split("infoboxtable",1)[1].split("</table>",1)[0]
                        except IndexError:
                            embed = discord.Embed(
                                title=re.search(self.title_regex, data.split("mw-body-content",1)[1].split("bodyContent",1)[0]).group(1),
                                url="https://astroneer.gamepedia.com/"+args.object
                            )
                            await message.channel.send(embed=embed)
                            return

                        embed = discord.Embed(
                            title=re.search(self.name_regex, data).group(1),
                            url="https://astroneer.gamepedia.com/"+args.object
                        )
                        embed.set_image(url=re.search(self.image_regex, data).group(1))

                        matches = re.finditer(self.field_regex, data)

                        for matchNum, match in enumerate(matches):
                            matchNum = matchNum + 1
                            if "<a" in match.group(1):
                                key = match.group(1).split("<a",1)[0] + " " + match.group(1).split(">",1)[-1].split("<")[0]
                            else:
                                key = match.group(1)
                            if "<a" in match.group(2):
                                value = match.group(2).split("<a",1)[0] + " " + match.group(2).split(">",1)[-1].split("<")[0]
                            else:
                                value = match.group(2)
                            embed.add_field(name=key, value=value)

                        await message.channel.send(embed=embed)
                except urllib.error.HTTPError:
                    await message.channel.send("That object doesn't exist!")
