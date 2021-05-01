import lox.shell as shell
import sys
import io
from lox.errors import Errors
from lox.scanner import Scanner
from lox.token import Token
from lox.tokentype import TokenType


def test_execute(mocker):
    mocker.patch.object(Scanner, 'scan_tokens', lambda *args, **kwargs: [
                        Token(TokenType.EOF, "", None, 1)])
    sys.stdout = io.StringIO()
    shell._execute("anything")
    assert sys.stdout.getvalue().strip() == 'TokenType.EOF "" 1'


def test_run_source_happy(mocker):
    Errors.had_error = False
    mocker.patch('builtins.open', side_effect=lambda file,
                 mode: io.StringIO("contents"))
    mocker.patch('lox.shell._execute')
    errno = shell.run("anything")
    assert errno == 0


def test_run_source_error(mocker):
    def have_an_error(*arg, **kwargs):
        Errors.had_error = True

    mocker.patch('builtins.open', side_effect=lambda file,
                 mode: io.StringIO("contents"))
    mocker.patch('lox.shell._execute', side_effect=have_an_error)
    errno = shell.run("anything")
    assert errno == 65


def test_run_interactive(mocker):
    looped = False

    def thrower(arg):
        nonlocal looped
        if looped:
            raise RuntimeError()
        looped = True

    mocker.patch('builtins.input', return_value="")
    mocker.patch('lox.shell._execute', side_effect=thrower)
    try:
        shell.run()
    except RuntimeError as e:
        assert e is not None


def test_main(mocker):
    mocker.patch('lox.shell.run', return_value=0)

    assert shell.main([]) == 0
    assert shell.main(["some_file.lox"]) == 0

    sys.stdout = io.StringIO()
    errno = shell.main(["too", "many", "args"])

    assert errno == 64
    assert sys.stdout.getvalue().strip() == "Usage: plox [script]"
