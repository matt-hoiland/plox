from lox.tokentype import TokenType
from lox.token import Token


def test_token():
    assert 'TokenType.AND "and" 1' == str(Token(TokenType.AND, "and", None, 1))
