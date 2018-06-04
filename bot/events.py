import inspect

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
