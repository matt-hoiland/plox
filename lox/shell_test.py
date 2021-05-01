from lox.shell import Shell

def test_run():
    """Test shell execution.

    Temporary testing code for project setup.
    """
    import sys, io
    sio = io.StringIO()
    sys.stdout = sio
    Shell().run()
    sys.stdout = sys.__stdout__
    assert sio.getvalue().strip() == "Hi! I'm the plox shell!"