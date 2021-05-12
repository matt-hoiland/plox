from lox.tokentype import TokenType
from lox.token import Token
from lox.scanner import Scanner
from lox.errors import Errors
import sys
import io


def test_scanner_symbols():
    scanner = Scanner("""// this is a comment
(( )){} // grouping stuff
!*+-/=<> <= == >= !=// operators
!""")

    rcv_tokens = scanner.scan_tokens()
    act_tokens = [
        Token(TokenType.LEFT_PAREN, "(", None, 2),
        Token(TokenType.LEFT_PAREN, "(", None, 2),
        Token(TokenType.RIGHT_PAREN, ")", None, 2),
        Token(TokenType.RIGHT_PAREN, ")", None, 2),
        Token(TokenType.LEFT_BRACE, "{", None, 2),
        Token(TokenType.RIGHT_BRACE, "}", None, 2),
        Token(TokenType.BANG, "!", None, 3),
        Token(TokenType.STAR, "*", None, 3),
        Token(TokenType.PLUS, "+", None, 3),
        Token(TokenType.MINUS, "-", None, 3),
        Token(TokenType.SLASH, "/", None, 3),
        Token(TokenType.EQUAL, "=", None, 3),
        Token(TokenType.LESS, "<", None, 3),
        Token(TokenType.GREATER, ">", None, 3),
        Token(TokenType.LESS_EQUAL, "<=", None, 3),
        Token(TokenType.EQUAL_EQUAL, "==", None, 3),
        Token(TokenType.GREATER_EQUAL, ">=", None, 3),
        Token(TokenType.BANG_EQUAL, "!=", None, 3),
        Token(TokenType.BANG, "!", None, 4),
        Token(TokenType.EOF, "", None, 4),
    ]

    for rcv, act in zip(rcv_tokens, act_tokens):
        assert rcv == act


def test_strings():
    scanner = Scanner("""// String tests
"I'm a string!"
"I'm a
multi-line
string!"
""")

    rcv_tokens = scanner.scan_tokens()
    act_tokens = [
        Token(TokenType.STRING, '"I\'m a string!"', "I'm a string!", 2),
        Token(TokenType.STRING, '"I\'m a\nmulti-line\nstring!"',
              "I'm a\nmulti-line\nstring!", 5),
        Token(TokenType.EOF, "", None, 6),
    ]

    for rcv, act in zip(rcv_tokens, act_tokens):
        assert rcv == act


def test_unterminated_string():
    scanner = Scanner('"No end in sight')

    sys.stderr = io.StringIO()
    tokens = scanner.scan_tokens()

    assert len(tokens) == 1
    assert "Unterminated" in sys.stderr.getvalue()
    assert Errors.had_error


def test_unexpected_character():
    scanner = Scanner('[')
    sys.stderr = io.StringIO()
    tokens = scanner.scan_tokens()

    assert len(tokens) == 1
    assert "Unexpected" in sys.stderr.getvalue()
    assert Errors.had_error


def test_numbers_happy():
    scanner = Scanner('123 123.0 123. .456 789.')
    received_tokens = scanner.scan_tokens()

    expected_tokens = [
        Token(TokenType.NUMBER, "123", 123, 1),
        Token(TokenType.NUMBER, "123.0", 123.0, 1),
        Token(TokenType.NUMBER, "123", 123, 1),
        Token(TokenType.DOT, ".", None, 1),
        Token(TokenType.DOT, ".", None, 1),
        Token(TokenType.NUMBER, "456", 456, 1),
        Token(TokenType.NUMBER, "789", 789, 1),
        Token(TokenType.DOT, ".", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]

    assert len(received_tokens) == len(expected_tokens)

    for received, expected in zip(received_tokens, expected_tokens):
        assert received == expected


def test_identifiers_happy():
    scanner = Scanner('_ _happy happy super bowl or superb owl')
    received_tokens = scanner.scan_tokens()

    expected_tokens = [
        Token(TokenType.IDENTIFIER, "_", None, 1),
        Token(TokenType.IDENTIFIER, "_happy", None, 1),
        Token(TokenType.IDENTIFIER, "happy", None, 1),
        Token(TokenType.SUPER, "super", None, 1),
        Token(TokenType.IDENTIFIER, "bowl", None, 1),
        Token(TokenType.OR, "or", None, 1),
        Token(TokenType.IDENTIFIER, "superb", None, 1),
        Token(TokenType.IDENTIFIER, "owl", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]

    assert len(received_tokens) == len(expected_tokens)

    for received, expected in zip(received_tokens, expected_tokens):
        assert received == expected
