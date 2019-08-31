#!/usr/bin/env python3
from curses import curs_set, echo, error, newpad, newwin, noecho, wrapper
from curses.textpad import Textbox
from os.path import isfile
from re import match
from sys import argv
from time import sleep


def main(stdscr):
    args = argv[1:]

    for i in range(len(args)):
        if isfile(args[i]):
            with open(args[i]) as file:
                args[i] = file.read()

    args = [shift([arg], 26) for arg in args]
    arg = args[0]
    curs_set(0)
    itermy, itermx = (i - 1 for i in stdscr.getmaxyx())
    y, x = padsize(args[0])
    pad = newpad(y, x)
    yinfo = 15
    info = newwin(yinfo, itermx + 1, itermy - (yinfo - 1), 0)
    info.keypad(True)
    ymaxscroll = y - itermy + (yinfo - 2)
    xmaxscroll = x - itermx
    ypos = 0
    xpos = 0
    iarg = 0
    keyhelp = ("D: increment shift\n"
            "A: decrement shift\n"
            "W: next argument\n"
            "S: previous argument\n"
            "H: scroll right\n"
            "J: scroll down\n"
            "K: scroll up\n"
            "L: scroll left\n"
            ": save\n"
            "Q: quit")

    while 1:
        pad.clear(); info.clear()

        while True:
            try:
                pad.addstr(f"{arg[arg[-1]]}")
                break
            except error:
                pad.clear()
                x = pad.getmaxyx()[1]
                pad.resize(y, x + 1)

        midstr(info, 1, f"ARGUMENT: {iarg}")
        midstr(info, 2, f"SHIFT: {arg[-1]}")
        midstr(info, 4, keyhelp)
        info.box()
        pad.refresh(ypos, 0, 0, 0, itermy - yinfo, itermx)
        info.refresh()
        char = info.getkey().lower()

        if char == "d":
            arg[-1] += 1

            if arg[-1] == 26:
                arg[-1] = 0
        elif char == "a":
            arg[-1] -= 1

            if arg[-1] == -1:
                arg[-1] = 25
        elif char in ["s", "w"]:
            if char == "s":
                iarg -= 1

                if iarg == -1:
                    iarg = args.index(args[-1])
            else:
                iarg += 1

                if iarg == len(args):
                    iarg = 0

            arg = args[iarg]
        elif char in ["j", "k"]:
            if y <= itermy:
                continue

            if char == "j":
                ypos += 1

                if ypos > ymaxscroll:
                    ypos = 0
            else:
                ypos -= 1

                if ypos < 0:
                    ypos = ymaxscroll
        elif char in ["h", "l"]:
            if char == "h":
                xpos -= 1

            if xpos == 0:
                xpos = xmaxscroll
        elif char == "l":
            xpos += 1

            if xpos > xmaxscroll:
                xpos = 0
        elif char == "":
            info.clear()
            info.box()
            midstr(info, 3, "output filename (default: output.txt):")
            mv(info, 1, -16)
            info.refresh()
            fname = str(scrinput(info), "utf-8")

            if fname == "":
                fname = "output.txt"

            if isfile(fname):
                midstr(info, 6, (f"Warning: {fname} exists.\n"
                    "N: cancel\n"
                    "A: append\n"
                    "Y: overwrite"))

                while True:
                    yn = info.getkey().lower()

                    if yn in ["n", "a", "y"]:
                        if yn == "a":
                            file = open(fname, "a")
                        elif yn == "y":
                            file = open(fname, "w")
                        break

                if yn == "n":
                    continue

            else:
                file = open(fname, "x")

            file.write(arg[arg[-1]])
            file.close()
        elif char == "q":
            raise KeyboardInterrupt


def padsize(arg):
    lines = arg[0].split("\n")
    y = len(lines)
    x = len(max(lines, key=len))
    return y, x

def midstr(window, inity, string):
    if len(string.splitlines()) > 1:
        lines = string.splitlines()
        x = (window.getmaxyx()[1] - len(lines[0]) - 1) // 2
        for line, y in zip(lines, range(inity, len(lines) + inity)):
            try:
                window.addstr(y, x, line)
            except:
                print(f"line: {line}; y: {y}")
        return

    x = (window.getmaxyx()[1] - len(string) - 1) // 2
    window.addstr(inity, x, string)


def mv(window, y=0, x=0):
    cury, curx = window.getyx()
    window.move(cury + y, curx + x)


def scrinput(window):
    curs_set(1)
    echo()
    string = window.getstr()
    curs_set(0)
    noecho()

    return string


def shift(variants, length):
    if len(variants) == length:
        variants.append(0)
        return variants

    text = [char for char in variants[-1]]

    for index in range(len(text)):
        char = text[index]

        if match(r"\s", char):
            continue

        text[index] = chr(ord(char) + 1)

    variants.append("".join(text))
    return shift(variants, length)


if len(argv[1:]) >= 1:
    try:
        wrapper(main)
    except KeyboardInterrupt:
        pass

