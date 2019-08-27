#!/usr/bin/env python3
from curses import curs_set, echo, newpad, newwin, noecho, wrapper
from os.path import isfile
from re import match
from sys import argv


def main(stdscr):
    args = argv[1:]
    for i in range(len(args)):
        if isfile(args[i]):
            with open(args[i]) as file:
                args[i] = file.read()
    args = [shift([arg], 26) for arg in args]
    curs_set(0)
    itermy = stdscr.getmaxyx()[0] - 1
    itermx = stdscr.getmaxyx()[1] - 1
    pad = newpad(*padsize(args[0]))
    info = newwin(13, itermx + 1, itermy - 12, 0)
    info.keypad(True)
    y = pad.getmaxyx()[0]
    maxscroll = y - itermy + 11
    pos = 0
    iarg = 0
    keys = ("D: increment shift\n"
            "A: decrement shift\n"
            "S: scroll down\n"
            "W: scroll up\n"
            ": save\n"
            "L: next argument\n"
            "H: previous argument\n"
            "Q: quit")

    while 1:
        arg = args[iarg]
        pad.clear(); info.clear()
        pad.addstr(f"{arg[arg[-1]]}")
        midstr(info, 1, f"ARGUMENT: {iarg}")
        midstr(info, 2, f"SHIFT: {arg[-1]}")
        midstr(info, 4, keys)
        info.box()
        pad.refresh(pos, 0, 0, 0, itermy - 11, itermx)
        info.refresh()
        char = info.getkey()

        if char.lower() == "d":
            arg[-1] += 1

            if arg[-1] == 26:
                arg[-1] = 0
        elif char.lower() == "a":
            arg[-1] -= 1

            if arg[-1] == -1:
                arg[-1] = 25
        elif char.lower() == "s":
            pos += 1

            if pos > maxscroll:
                pos = 0
        elif char.lower() == "w":
            pos -= 1

            if pos < 0:
                pos = maxscroll
        elif char == "":
            info.clear()
            info.box()
            midstr(info, 3, "output filename:")
            mv(info, 1, -16)
            info.refresh()
            fname = scrinput(info)

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
        elif char.lower() == "l":
            iarg += 1

            if iarg == len(args):
                iarg = 0
        elif char.lower() == "h":
            iarg -= 1

            if iarg == -1:
                iarg = args.index(args[-1])
        elif char.lower() == "q":
            raise KeyboardInterrupt


def padsize(arg):
    lines = arg[0].split("\n")
    y = len(lines)
    x = len(max(lines, key=len)) * 2
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

