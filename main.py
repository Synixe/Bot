import sys
import os

class App:
    def installdeps(self):
        try:
            import pip
        except:
            print("pip is not installed")
            sys.exit(1)
        if os.path.exists("deps.txt"):
            deps = ""
            with open("deps.txt") as deptxt:
                deps = deptxt.read().split("\n")
            for dep in deps:
                if dep.strip() != "":
                    pip.main(["install", dep, "--upgrade"])
            import hashlib
            with open(".data/deps.md5", "w") as dephash:
                dephash.write(hashlib.md5(open("deps.txt", 'rb').read()).hexdigest())
        else:
            print("deps.txt is missing")
            sys.exit(1)

    def run(self):
        parser = argparse.ArgumentParser(description="BotMio Core")
        parser.add_argument("profile", help="Bot profile to load")
        parser.add_argument("--debug", action="store_true", help="Display debug logs in the terminal")
        args = parser.parse_args()

        if not os.path.exists(".data/"):
            os.mkdir(".data/")

        try:
            import logger
        except ModuleNotFoundError:
            print("Running first time setup")
            self.installdeps()
            import logger

        logger.set_debug(args.debug)

        if not os.path.exists(".data/deps.md5"):
            logger.debug("No dependency hashes, reinstall dependencies")
            self.installdeps()
        else:
            with open(".data/deps.md5") as dephash:
                import hashlib
                logger.debug("Comparing dependency hashes")
                if hashlib.md5(open("deps.txt", 'rb').read()).hexdigest() != dephash.read().strip():
                    logger.info("Updating Dependencies")
                    self.installdeps()

        logger.clear()
        logger.info("Starting")

        profilepath = ".profiles/{}.json".format(args.profile)
        if os.path.exists(profilepath):
            import json
            logger.debug("Reading profile from {}".format(profilepath))
            with open(profilepath) as profile:
                from bot import Profile
                self.profile = Profile(json.load(profile))
            logger.info("Profile: {}".format(self.profile.name))
        else:
            logger.error("The profile {} does not exist.".format(args.profile))
            sys.exit(4)

        import client
        self.bot = client.Client()
        self.bot.profile = self.profile
        self.bot.run(self.profile.tokens["discord"])

if __name__ == "__main__":
    app = App()

    try:
        from os import environ
        environ['SHELL']
    except KeyError:
        print("The Windows CMD is not supported. Please use a shell like Git Bash.")
        sys.exit(1)

    import argparse

    try:
        import logger
    except:
        pass

    app.run()
