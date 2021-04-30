#!/usr/bin/env python3

import sys

from lox.scanner import Scanner
import lox.error as err

__AUTHOR__ = 'Matt Hoiland'
__PROGRAM__ = 'plox'
__VERSION__ = 'v0.1.0'
__YEAR__ = '2021'


def main(argv: list[str]) -> None:
    if len(argv) > 2:
        print('Usage: python3 lox/Lox.py [script]')
        sys.exit(64)
    elif len(argv) == 2:
        run_file(argv[1])
    else:
        run_prompt()


def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(token)


def run_file(path):
    with open(path, 'r') as fp:
        source = fp.read()
    run(source)
    if err.had_error:
        sys.exit(65)


def run_prompt():
    print(f'{__PROGRAM__}@{__VERSION__} (c) {__YEAR__} by {__AUTHOR__}')
    print("Use `:help' for interpreter command list.")

    commands = {}

    def exit_command():
        """exits interactive reple and stops interpreter"""
        sys.exit(0)

    def help_command():
        """displays this help message"""
        for k in commands:
            print(f'{k}\t{commands[k].__doc__}')

    commands[':exit'] = exit_command
    commands[':help'] = help_command

    while True:
        line = input('> ')
        if line in commands:
            commands[line]()
        else:
            run(line)
            had_error = False
