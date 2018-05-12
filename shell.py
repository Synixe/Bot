def open(**kwargs):
    print("Open is not allowed in the interactive shell")

buffer = ""

while True:
    code = input("")
    buffer += code + "\n"
    if buffer.endswith("||END||\n"):
        try:
            exec(buffer.rstrip("||END||\n"))
        except:
            pass
        buffer = ""
