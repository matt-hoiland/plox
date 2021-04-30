#!/usr/bin/env python3

from lox.token_type import TokenType

class Token:
    def __init__(self, ttype: TokenType, lexeme: str, literal: object, line: int) -> None:
        self.type: TokenType = ttype
        self.lexeme: str = lexeme
        self.literal: object = literal
        self.line: int = line

    def __str__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'