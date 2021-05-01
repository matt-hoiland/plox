"""Lox Interpreter"""

from lox.scanner import Scanner
from typing import List
from lox.errors import Errors


def _execute(source: str):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)


def run(source_file=None) -> int:
    """Start the interpreter"""
    if source_file is not None:
        fp = open(source_file, 'r')
        source = fp.read()
        fp.close()
        _execute(source)
        if Errors.had_error:
            return 65  # some error code
        return 0

    while True:
        line = input("> ")
        _execute(line)
        Errors.had_error = False


def main(args: List[str]) -> int:
    if len(args) > 1:
        print("Usage: plox [script]")
        return 64  # some error code
    if len(args) == 1:
        return run(args[0])
    return run()
