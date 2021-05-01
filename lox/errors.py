import sys


class Errors:
    had_error: bool = False

    @classmethod
    def error(cls, line: int, message: str):
        cls._report(line, "", message)

    @classmethod
    def _report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}", file=sys.stderr)
        cls.had_error = True
