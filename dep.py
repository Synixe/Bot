"""Helps the user install missing dependencies"""
import logger
def ask(lib):
    """Ask the user if they want to install a dependency"""
    logger.error("You are missing {}, would you like to download it?".format(lib))
    if input("(Y/N): ").lower() == "y":
        from sys import platform
        import os
        if platform == "linux" or platform == "linux2":
            os.system("sudo python3 -m pip install {}".format(lib))
        else:
            os.system("python -m pip install {}".format(lib))
        return True
    else:
        return False
