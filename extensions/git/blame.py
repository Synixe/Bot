import subprocess

def blame(ext, command):
    try:
        data = subprocess.getoutput("git blame extensions/"+ext+"/__init__.py").split("\n")
        authors = {}
        reading = False
        start_line = 0
        end_line = 0
        x = 0
        for l in data:
            x += 1
            a = l.split(")", 1)
            author = a[0].split("(")[1].split(" 20")[0].split(" ")[0]
            line = a[1].strip()
            if reading and line.startswith("async def"):
                reading = False
                end_line = x - 2
            if line.startswith("async def "+command):
                reading = True
                start_line = x
            elif reading:
                if author not in authors:
                    authors[author] = 1
                else:
                    authors[author] += 1
        return authors, start_line, end_line
    except IndexError:
        return "That command is being developed right now and doesn't have git information yet.", None, None

if __name__ == "__main__":
    import sys
    print(blame(sys.argv[1], sys.argv[2]))
