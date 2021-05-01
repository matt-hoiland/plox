from lox.tokentype import TokenType
from typing import List

from lox.token import Token
from lox.errors import Errors


class UnimplementedError(RuntimeError):
    pass


class Scanner:
    _current: int
    _line: int
    _source: str
    _start: int
    _tokens: List[Token]

    def __init__(self, source: str):
        self._current = 0
        self._line = 1
        self._source = source
        self._start = 0
        self._tokens = []

    def _add_token(self, ttype: TokenType, literal: object = None):
        text = self._source[self._start:self._current]
        self._tokens.append(Token(ttype, text, literal, self._line))

    def _advance(self) -> str:
        c = self._source[self._current]
        self._current += 1
        return c

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self._source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self._source[self._current]

    def _scan_token(self):
        c = self._advance()

        cases = {
            "(": lambda: self._add_token(TokenType.LEFT_PAREN),
            ")": lambda: self._add_token(TokenType.RIGHT_PAREN),
            "{": lambda: self._add_token(TokenType.LEFT_BRACE),
            "}": lambda: self._add_token(TokenType.RIGHT_BRACE),
            ",": lambda: self._add_token(TokenType.COMMA),
            ".": lambda: self._add_token(TokenType.DOT),
            "-": lambda: self._add_token(TokenType.MINUS),
            "+": lambda: self._add_token(TokenType.PLUS),
            ";": lambda: self._add_token(TokenType.SEMICOLON),
            "*": lambda: self._add_token(TokenType.STAR),
            "!": lambda: self._add_token(TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG),
            "=": lambda: self._add_token(TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL),
            "<": lambda: self._add_token(TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS),
            ">": lambda: self._add_token(TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER),
            "/": self.__slash_case,
            "\"": self.__string_case,
        }

        if c in (" ", "\r", "\t"):
            return
        if c == "\n":
            self._line += 1
            return
        if c not in cases:
            Errors.error(self._line, "Unexpected character.")
            return
        cases[c]()

    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens

    def __slash_case(self):
        if not self._match("/"):  # Not a comment.
            self._add_token(TokenType.SLASH)
            return
        # Is a comment. Consume comment.
        while self._peek() != "\n" and not self._is_at_end():
            self._advance()

    def __string_case(self):
        while self._peek() != "\"" and not self._is_at_end():
            if self._peek() == "\n":
                self._line += 1
            self._advance()

        if self._is_at_end():
            Errors.error(self._line, "Unterminated string.")
            return

        # The closing ".
        self._advance()

        value = self._source[self._start+1:self._current-1]
        self._add_token(TokenType.STRING, value)
