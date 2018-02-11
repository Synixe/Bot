import zipfile, os, sys
import shutil
import urllib.request
import time

try:
    import discord
    print("Removing Discord.py")
    os.system("python -m pip uninstall discord.py")
except:
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
