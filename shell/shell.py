import sys

def open(**kwargs):
    print("Open is not allowed in the interactive shell")

buffer = ""

pyinput = input

def input(text):
    return pyinput(text).rstrip("||END||")

while True:
    code = pyinput()
    buffer += code + "\n"
    if buffer.endswith("||END||\n"):
        try:
            exec(buffer.rstrip("||END||\n"))
        except:
            pass
        buffer = ""
