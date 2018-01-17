import datetime
import time

def clear():
    with open("bot.log",'w') as f:
        f.write("")

def info(text):
    with open("bot.log",'a') as f:
        f.write("[INFO]["+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"] ")
        f.write(str(text))
        f.write("\n")
