"""Github Blame Command"""
import subprocess

def blame(ext, command):
    """Find a function and get the number of lines created by each author"""
    try:
        data = subprocess.getoutput("git blame extensions/"+ext+"/__init__.py").split("\n")
        authors = {}
        reading = False
        start_line = 0
        end_line = 0
        count = 0
        for raw_line in data:
            count += 1
            raw_author = raw_l.split(")", 1)
            author = raw_author[0].split("(")[1].split(" 20")[0].split(" ")[0]
            line = raw_author[1].strip()
            if reading and line.startswith("async def"):
                reading = False
                end_line = count - 2
            if line.startswith("async def "+command):
                reading = True
                start_line = count
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
