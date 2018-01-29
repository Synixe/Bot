import random

path = "/media/sydney/web/gifs/"

class GifDirectories:
    treason = ["starwars","kylo","blacksails"]
    spelling = ["writingishard","tenor","clapping"]

def process(value):
    return path+value+".gif"

def getRandom(category):
    try:
        return process(category+"/"+random.choice(getattr(GifDirectories, category)))
    except:
        return process(category+"/"+random.choice(GifDirectories.spelling))
