import inspect
import discord
import copy
import logger
import sys

class ArgumentException(Exception):
    def __init__(self, text, data):
        super().__init__(text)
        self.data = data

class Extension:
    pass

class Arguments:
    def __init__(self, ctx, raw, args):
        self._ctx = ctx
        self._raw = raw
        self._args = args
        self._values = []

        self._usage = " ".join([x[0] for x in args])

        current = 0

        for arg in self._args:
            if arg[0].startswith("[") and arg[0].endswith("]"):
                if current < len(raw):
                    if arg[0][-2] == "+":
                        value = self._parse(arg, " ".join(raw[current:]))
                        setattr(self, arg[0][1:-2], value)
                        current = len(raw)
                    else:
                        value = self._parse(arg, raw[current])
                        setattr(self, arg[0][1:-1], value)
                        current += 1
                else:
                    setattr(self, arg[0][1:-1], arg[2])
                    if arg[0][-2] == "+":
                        setattr(self, arg[0][1:-2], arg[2])
                    else:
                        setattr(self, arg[0][1:-1], arg[2])
            else:
                if current == len(raw):
                    raise ArgumentException("Not Enough Args", [self, arg[0]])
                else:
                    if arg[0][-1] == "+":
                        value = self._parse(arg, " ".join(raw[current:]))
                        setattr(self, arg[0][:-1], value)
                        current = len(raw)
                    else:
                        value = self._parse(arg, raw[current])
                        setattr(self, arg[0], value)
                        current += 1

        self._ctx = None
        del self._ctx

    def _parse(self, arg, value):
        argtype = arg[1]
        arg = arg[0]
        if argtype == Command:
            for ext in self._ctx._bot.extensions:
                for c in ext.commands:
                    if c.name == value:
                        c.extension = ext
                        return c
            raise ArgumentException("Invalid Command", [self, arg, value])
        elif argtype == discord.Member:
            if value.startswith("<@"):
                value = value[2:-1]
                if value.startswith("!"):
                    value = value[1:]
            try:
                value = int(value)
                member = self._ctx.message.channel.guild.get_member(value)
            except:
                value = value.lower()
                member = discord.utils.find(lambda m: m.name.lower() == value or m.display_name.lower() == value, self._ctx.message.channel.guild.members)
                if member == None:
                    raise ArgumentException("Member Not Found", [self, arg, value])
            if member == None:
                raise ArgumentException("Member Not Found", [self, arg, value])
            return member
        elif argtype == discord.Role:
            role = discord.utils.find(lambda m: m.name.lower() == value.lower() or str(m.id) == value, self._ctx.message.channel.guild.roles)
            if role == None:
                raise ArgumentException("Role Not Found", [self, arg, value])
            return role
        elif argtype == int:
            try:
                value = int(value)
            except:
                try:
                    value = self._txt2int(value)
                except:
                    raise ArgumentException("TypeError", [self, arg, value, "number"])
        return value

    def _txt2int(self, textnum, numwords={}):
        if not numwords:
          units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
          ]
          tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
          scales = ["hundred", "thousand", "million", "billion", "trillion"]
          numwords["and"] = (1, 0)
          for idx, word in enumerate(units):    numwords[word] = (1, idx)
          for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
          for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)
        current = result = 0
        for word in textnum.split():
            if word not in numwords:
                raise Exception("Illegal word: " + word)
            scale, increment = numwords[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
        return result + current

class Command:
    def __init__(self, name, callback, **kwargs):
        self.func = callback
        self.name = name

        self.roles = ["@everyone"]
        self.args = []
        self.usage = " ".join([x[0] for x in self.args])

        self.file = kwargs.get("file")
        self.help = kwargs.get("help")

        with open(self.file) as source:
            lines = source.read().split("\n")
            for l in range(len(lines)):
                line = lines[l]
                if line.strip().startswith("async def {}(".format(self.func.__name__)):
                    for i in range(l - 1, 0, -1):
                        if lines[i].strip().startswith("@"):
                            self.start = i + 1
                        else:
                            break
                    self.end = len(lines) - 1
                    for i in range(l, len(lines)):
                        if lines[i].strip().startswith("@") or lines[i].strip().startswith("class "):
                            self.end = i - 1
                            break

    async def run(self, ctx, args):
        if self.args == []:
            ctx.args = None
            await self.func(ctx, ctx.message)
            return
        try:
            ctx.args = Arguments(ctx, args, self.args)
            await self.func(ctx.safe(), ctx.message)
        except ArgumentException as e:
            if str(e) == "Invalid Command":
                embed = discord.Embed(
                    title="Command Not Found",
                    description="The command `{}` provided for `{}` was not found".format(e.data[2], e.data[1])
                )
                embed.set_footer(text="Usage: {0._ctx.profile.prefix}{1} {0._usage}".format(e.data[0], self.name))
            elif str(e) == "Not Enough Args":
                embed = discord.Embed(
                    title="Missing {}".format(e.data[1]),
                    description="`{}` is a required field".format(e.data[1])
                )
                embed.set_footer(text="Usage: {0._ctx.profile.prefix}{1} {0._usage}".format(e.data[0], self.name))
            elif str(e) == "Member Not Found":
                embed = discord.Embed(
                    title="Member Not Found",
                    description="The user `{}` was not found.".format(e.data[2])
                )
            elif str(e) == "Role Not Found":
                embed = discord.Embed(
                    title="Role Not Found",
                    description="The role `{}` was not found.".format(e.data[2])
                )
            elif str(e) == "TypeError":
                embed = discord.Embed(
                    title="Invalid Type",
                    description="`{}` must be a {}".format(e.data[1], e.data[3])
                )
            await ctx.message.channel.send(embed=embed)

def command(name=None, **attrs):
    def decorator(func):
        frame = inspect.stack()[1]
        attrs["file"] = frame[1]
        attrs["lineno"] = frame[2]
        if isinstance(func, Command):
            raise TypeError('Callback is already a command.')
        import asyncio
        if not asyncio.iscoroutinefunction(func):
            raise TypeError('Callback must be a coroutine.')
        help_doc = attrs.get('help')
        if help_doc is not None:
            help_doc = inspect.cleandoc(help_doc)
        else:
            help_doc = inspect.getdoc(func)
            if isinstance(help_doc, bytes):
                help_doc = help_doc.decode('utf-8')
        attrs['help'] = help_doc
        fname = name or func.__name__
        return Command(name=fname, callback=func, **attrs)
    return decorator

class EventHandler:
    def __init__(self, name, callback, **kwargs):
        self.func = callback
        self.name = name

        self.event = kwargs.get("event")

        self.file = kwargs.get("file")
        self.lineno = kwargs.get("lineno")
        self.help = kwargs.get("help")

    async def run(self, ctx):
        await self.func(ctx.safe(), ctx.message)

def event(event, **attrs):
    def decorator(func):
        frame = inspect.stack()[1]
        attrs["file"] = frame[1]
        attrs["lineno"] = frame[2]
        attrs["event"] = event
        if isinstance(func, EventHandler):
            raise TypeError("Callback is already a event handler.")
        import asyncio
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Callback must be a coroutine.")
        help_doc = attrs.get('help')
        if help_doc is not None:
            help_doc = inspect.cleandoc(help_doc)
        else:
            help_doc = inspect.getdoc(func)
            if isinstance(help_doc, bytes):
                help_doc = help_doc.decode('utf-8')
        attrs['help'] = help_doc
        return EventHandler(name=func.__name__, callback=func, **attrs)
    return decorator

def role(role):
    def decorator(func):
        if len(func.roles) == 1 and func.roles[0] == "@everyone":
            func.roles = [role]
        else:
            func.roles.append(role)
        return func
    return decorator

def argument(name, argtype=str, default=None):
    def decorator(func):
        func.args.append([name, argtype, default])
        func.usage = " ".join([x[0] for x in func.args])
        return func
    return decorator

class Context:
    def __init__(self, bot, extension, message):
        self.user = bot.user
        self.profile = bot.profile
        self.extension = extension
        self.message = message
        self.loop = bot.loop

        self._bot = bot

    def safe(self):
        safe = copy.copy(self)
        self._bot = None
        del self._bot
        return safe

class Profile:
    def __init__(self, data):
        for req in ["name", "mode", "prefix", "tokens"]:
            if req not in data:
                logger.error("Invalid Profile: Missing '{}'".format(req))
                sys.exit(2)

        if data["mode"] not in ["test","live"]:
            logger.error("Invalid Profile Mode: {}".format(data["mode"]))
            sys.exit(3)

        self.name = data["name"]
        self.mode = data["mode"]
        self.prefix = data["prefix"]
        self.tokens = data["tokens"]

def in_role_list(member, roles):
    """Check if a member is in a list of roles"""
    if "@everyone" in roles:
        return True
    if isinstance(member, discord.User):
        return False
    for role in member.roles:
        if role.name.lower() in roles:
            return True
    return False

async def send_stats(c, prefix, resp, raw, channel):
    printing = False
    header = False
    inside = False
    text = ""
    info = ""
    for line in resp:
        if line.strip().startswith("File: {}".format(c.file)):
            printing = True
        elif line.strip().startswith("File:"):
            printing = False
        elif printing and line.startswith("----"):
            header = True
        if printing and not header:
            if not line.startswith("Line #"):
                info += line + "\n"
        elif printing and not inside:
            if line.split("|",1)[0].strip() == str(c.start - 1):
                inside = True
        elif printing and inside:
            if line.split("|",1)[0].strip() == str(c.end + 1):
                inside = False
            if inside:
                fields = line.split("|")
                data = [x.strip() for x in fields[:-1]]
                if len(data) == 0:
                    continue
                if data[0] != "(call)":
                    data.append(fields[-1][4:])
                else:
                    try:
                        data.append("#"+fields[-1].split("site-packages/")[1])
                    except IndexError:
                        data.append("#"+fields[-1])
                del fields
                dec =  "{}{}: {} ({}, {})".format(data[0], " " * (6 - len(data[0])), data[1], data[2], data[4])
                text += "{}{}| {}".format(dec, " " * (30 - len(dec)), data[-1]) + "\n"
    embed = discord.Embed(
        title="{}{} {}".format(prefix, c.name, " ".join(raw[1:])),
        description=info
    )
    await channel.send("```py\n"+text+"```", embed=embed)
