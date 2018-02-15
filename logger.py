"""Logs to a file and outputs to the console with colors"""
import datetime
import time
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf8', buffering=1)

DEBUG = False

if sys.platform == "win32":
    from ctypes import windll, Structure, c_short, c_ushort, byref

    class COORD(Structure):
        """struct in wincon.h."""
        _fields_ = [
            ("X", c_short),
            ("Y", c_short)
        ]

    class RECT(Structure):
        """struct in wincon.h."""
        _fields_ = [
            ("Left", c_short),
            ("Top", c_short),
            ("Right", c_short),
            ("Bottom", c_short)
        ]

    class BUFFER(Structure):
        """struct in wincon.h."""
        _fields_ = [
            ("dwSize", COORD),
            ("dwCursorPosition", COORD),
            ("wAttributes", c_ushort),
            ("srWindow", RECT),
            ("dwMaximumWindowSize", COORD)
        ]

    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    HANDLE = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    FOREGROUND_BLUE      = 0x0001
    FOREGROUND_GREEN     = 0x0002
    FOREGROUND_RED       = 0x0004
    FOREGROUND_YELLOW    = 0x0006
    FOREGROUND_GREY      = 0x0007
    FOREGROUND_INTENSITY = 0x0008

    def get_text_attr():
        """Get text attritubes"""
        csbi = BUFFER()
        windll.kernel32.GetConsoleScreenBufferInfo(HANDLE, byref(csbi))
        return csbi.wAttributes

    def set_text_attr(color):
        """Set text color on windows"""
        windll.kernel32.SetConsoleTextAttribute(HANDLE, color)

def clear():
    """Empty the log file"""
    with open("bot.log", 'w') as f:
        f.write("")

def write(tag, text):
    """Write to the log file"""
    text = "["+tag+"]["+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"] " + str(text)
    sys.stdout.write(text+"\n")
    with open("bot.log", 'a') as f:
        f.write(text+"\n")

def info(text, c="grey"):
    """Info, Always Displayed"""
    color(c)
    write("INFO", text)
    color("reset")
def error(text, c="red"):
    """Error, Always Displayed"""
    color(c)
    write("ERRO", text)
    color("reset")
def debug(text, c="blue"):
    """Debug Information"""
    if DEBUG:
        color(c)
        write("DBUG", text)
        color("reset")

def set_debug(debug):
    """Set the debug setting"""
    global DEBUG
    DEBUG = debug

def color(color):
    """Set the text color"""
    if sys.platform == "win32":
        if color == "green":
            set_text_attr(FOREGROUND_GREEN | get_text_attr() & 0x0070 | FOREGROUND_INTENSITY)
        elif color == "yellow":
            set_text_attr(FOREGROUND_YELLOW | get_text_attr() & 0x0070 | FOREGROUND_INTENSITY)
        elif color == "red":
            set_text_attr(FOREGROUND_RED | get_text_attr() & 0x0070 | FOREGROUND_INTENSITY)
        elif color == "blue":
            set_text_attr(FOREGROUND_BLUE | get_text_attr() & 0x0070 | FOREGROUND_INTENSITY)
        elif color == "reset":
            set_text_attr(FOREGROUND_GREY | get_text_attr() & 0x0070)
        elif color == "grey":
            set_text_attr(FOREGROUND_GREY | get_text_attr() & 0x0070)
    else:
        if color == "green":
            sys.stdout.write('\033[92m')
        elif color == "red":
            sys.stdout.write('\033[91m')
        elif color == "blue":
            sys.stdout.write('\033[94m')
        elif color == "reset":
            sys.stdout.write('\033[0m')

try:
    import emoji
except ImportError:
    error("You are missing emoji, would you like to download it?")
    if input("(Y/N): ").lower() == "y":
        from sys import platform
        import os
        if platform == "linux" or platform == "linux2":
            os.system("sudo python3 -m pip install emoji")
        else:
            os.system("python -m pip install emoji")
        try:
            import emoji
            info("emoji Installed!", "green")
        except ImportError:
            error("Failed to install emoji")
    else:
        error("emoji is required")
        sys.exit(1)

def write(tag, text):
    """Write to the log file"""
    text = "["+tag+"]["+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"] " + str(text)
    sys.stdout.write(emoji.emojize(text, use_aliases=True)+"\n")
    sys.stdout.flush()
    with open("bot.log", 'a') as f:
        f.write(text+"\n")

def loading(text):
    sys.stdout.write(emoji.emojize(text, use_aliases=True))
