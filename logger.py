"""Logs to a file and outputs to the console with colors"""
import datetime
import time
import sys

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

    FOREGROUND_BLUE      = 0x0001
    FOREGROUND_GREEN     = 0x0002
    FOREGROUND_RED       = 0x0004
    FOREGROUND_YELLOW    = 0x0006
    FOREGROUND_GREY      = 0x0007
    FOREGROUND_INTENSITY = 0x0008

    def get_text_attr():
        csbi = BUFFER()
        windll.kernel32.GetConsoleScreenBufferInfo(HANDLE, byref(csbi))
        return csbi.wAttributes

    def set_text_attr(color):
        windll.kernel32.SetConsoleTextAttribute(HANDLE, color)

def clear():
    with open("bot.log", 'w') as f:
        f.write("")

def write(tag, text):
    text = "["+tag+"]["+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"] " + str(text)
    print(text)
    with open("bot.log", 'a') as f:
        f.write(text+"\n")

def info(text, c="grey"):
    color(c)
    write("INFO", text)
    color("reset")
def error(text, c="red"):
    color(c)
    write("ERRO", text)
    color("reset")
def debug(text, c="blue"):
    if DEBUG:
        color(c)
        write("DBUG", text)
        color("reset")

def set_debug(debug):
    global DEBUG
    DEBUG = debug

def color(color):
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
