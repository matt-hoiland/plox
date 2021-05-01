# plox

Python3 implementation of the tree walk interpreter from Robert Nystrom's book [Crafting Interpreters](https://craftinginterpreters.com/)

## Setup

Prequisite: `virtualenv`

```bash
$ virtualenv venv
$ source ./venv/bin/activate
(venv)$ pip install -r requirements.txt
```

## Run

The script `./plox` should already be executable. It can be invoked directly.

```bash
(venv)$ ./plox
```

If not, you can use the `Makefile`

```bash
(venv)$ make run
```

## Run tests

```bash
(venv)$ make test
```