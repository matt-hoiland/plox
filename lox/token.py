from dataclasses import dataclass
from lox.tokentype import TokenType


@dataclass(frozen=True)
class Token:
    ttype: TokenType
    lexeme: str
    literal: object
    line: int

    def __str__(self):
        return f"{self.ttype} \"{self.lexeme}\" {self.line}"
