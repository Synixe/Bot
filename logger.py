import datetime
import time

def clear():
    with open("bot.log",'w') as f:
        f.write("")

def write(tag, text):
    with open("bot.log",'a') as f:
        f.write("["+tag+"]["+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"] ")
        f.write(str(text))
        f.write("\n")

def info(text):
    write("INFO", text)
def error(text):
    write("ERRO", text)
