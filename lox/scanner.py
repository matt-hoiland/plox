#!/usr/bin/env python3

from lox.token import Token
from lox.token_type import TokenType
import lox.error as err

KEYWORDS = {
    'and': TokenType.AND,
    'class': TokenType.CLASS,
    'else': TokenType.ELSE,
    'false': TokenType.FALSE,
    'for': TokenType.FOR,
    'fun': TokenType.FUN,
    'if': TokenType.IF,
    'nil': TokenType.NIL,
    'or': TokenType.OR,
    'print': TokenType.PRINT,
    'return': TokenType.RETURN,
    'super': TokenType.SUPER,
    'this': TokenType.THIS,
    'true': TokenType.TRUE,
    'var': TokenType.VAR,
    'while': TokenType.WHILE,
}

class Scanner:
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._tokens: list[Token] = []
        self._start: int = 0
        self._current: int = 0
        self._line: int = 1

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, '', None, self._line))
        return self._tokens

    def _add_token(self, ttype: TokenType, literal: object = None) -> None:
        text: str = self._source[self._start:self._current]
        self._tokens.append(Token(ttype, text, literal, self._line))

    def _advance(self) -> str:
        c: str = self._source[self._current:self._current+1]
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
            return '\0'
        return self._source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return '\0'
        return self._source[self._current + 1]

    def _scan_token(self) -> None:
        c: str = self._advance()

        isdigit = lambda x: x.isdigit()
        isalpha = lambda x: x.isalpha() or x == '_'
        isalnum = lambda x: isdigit(x) or isalpha(x)

        def identifier_action():
            while isalnum(self._peek()):
                self._advance()

            text: str = self._source[self._start:self._current]
            ttype: TokenType = KEYWORDS.get(text, None)
            if ttype is None:
                ttype = TokenType.IDENTIFIER

            self._add_token(ttype, text)

        def increment_line_action():
            self._line += 1

        def noop_action(): pass

        def number_action():
            while isdigit(self._peek()):
                self._advance()

            # Look for a fractional part.
            if self._peek() == '.' and isdigit(self._peek_next()):
                # Consume the "."
                self._advance()

                while isdigit(self._peek()):
                    self._advance()

            self._add_token(TokenType.NUMBER, float(
                self._source[self._start:self._current]))

        def slash_action():
            if self._match('/'):
                # A comment goes until the end of the line.
                while self._peek() != '\n' and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)

        def string_action():
            while self._peek() != '"' and not self._is_at_end():
                if self._peek() == '\n':
                    increment_line_action()
                self._advance()

            if self._is_at_end():
                err.error(self._line, "Unterminiated string.")
                return

            # The closing ".
            self._advance()

            value: str = self._source[self._start + 1:self._current - 1]
            self._add_token(TokenType.STRING, value)

        token_map = {
            # Single character lexemes
            '(': lambda: self._add_token(TokenType.LEFT_PAREN),
            ')': lambda: self._add_token(TokenType.RIGHT_PAREN),
            '{': lambda: self._add_token(TokenType.LEFT_BRACE),
            '}': lambda: self._add_token(TokenType.RIGHT_BRACE),
            ',': lambda: self._add_token(TokenType.COMMA),
            '.': lambda: self._add_token(TokenType.DOT),
            '-': lambda: self._add_token(TokenType.MINUS),
            '+': lambda: self._add_token(TokenType.PLUS),
            ';': lambda: self._add_token(TokenType.SEMICOLON),
            '*': lambda: self._add_token(TokenType.STAR),

            # Single and double character lexemes
            '!': lambda: self._add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG),
            '=': lambda: self._add_token(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL),
            '<': lambda: self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS),
            '>': lambda: self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER),

            # Special slash (/) case
            '/': slash_action,

            # Ignore whitespace, but increment on new lines
            ' ': noop_action,
            '\r': noop_action,
            '\t': noop_action,
            '\n': increment_line_action,

            # Multicharacter lexemes
            '"': string_action,
        }

        def default_action():
            if isdigit(c):
                number_action()
            elif isalpha(c):
                identifier_action()
            else:
                err.error(self._line, f'Unexpected character: {c}')

        token_map.get(c, default_action)()
