"""Setups discord.py from the latest commit on rewrite"""
import sys
if sys.platform == "win32":
    import zipfile, os
    import shutil
    import urllib.request
    import time

    try:
        import discord
        print("Removing Discord.py")
        os.system("python -m pip uninstall discord.py")
    except ModuleNotFoundError:
        pass

    print("Downloading Discord.py rewrite")
    urllib.request.urlretrieve("https://github.com/Rapptz/discord.py/archive/rewrite.zip", "discord.zip")
    z = zipfile.ZipFile("discord.zip")
    z.extractall()

    os.chdir("discord.py-rewrite")
    os.system("python setup.py install")
    os.chdir("../")
    shutil.rmtree('discord.py-rewrite')
    print("Cleaning Up")
    z.close()
    time.sleep(1)
    os.remove("discord.zip")

    print("Installed!")
else:
    print("This script is for use on Windows only")
