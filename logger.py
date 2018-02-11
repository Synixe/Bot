import datetime
import time

def clear():
    with open("bot.log",'w') as f:
        f.write("")

def write(tag, text):
    text = "["+tag+"]["+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"] " + str(text)
    print(text)
    with open("bot.log",'a') as f:
        f.write(text+"\n")

def info(text):
    write("INFO", text)
def error(text):
    write("ERRO", text)
