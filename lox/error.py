#!/usr/bin/env python3

had_error = False


def error(line, message):
    report(line, "", message)


def report(line, where, message):
    print(f'[line {line}] Error{where}: {message}')
    had_error = True
