import logger
import sys

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
