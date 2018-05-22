import logger
import bot

import sys
import os
import importlib
import inspect

def get(dir):
    extlist = []
    if sys.platform == "linux" or sys.platform == "linux2":
        extensions = [x[0].split('/')[1] for x in os.walk(dir) if x[0].count('/') == 1 and "__pycache__" not in x[0]]
    else:
        extensions = [x[0].split('\\')[-1] for x in os.walk('./{}'.format(dir)) if x[0].count('/') == 1 and "__pycache__" not in x[0]][1:]
    for ext in extensions:
        extname = "{}.{}".format(dir, ext)
        #try:
        ext = importlib.import_module(extname)
        logger.debug("  {}".format(extname))
        #except:
        #    logger.error("Load Failed: {}".format(extname))
        #    continue
        clsmembers = inspect.getmembers(sys.modules[extname], inspect.isclass)
        for c in clsmembers:
            if issubclass(c[1], bot.Extension):
                logger.debug("    {0[0]}".format(c))
                c[1].commands = []
                c[1].handlers = []
                c[1].fullname = str(c[1]).split("'",2)[1]
                for method in inspect.getmembers(c[1]):
                    if isinstance(method[1], bot.Command):
                        c[1].commands.append(method[1])
                    elif isinstance(method[1], bot.EventHandler):
                        c[1].handlers.append(method[1])
                extlist.append(c[1])
    return extlist
