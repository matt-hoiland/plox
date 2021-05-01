PYTHON=python3

.PHONY: run
run:
	$(PYTHON) plox

.PHONY: test
test:
	$(PYTHON) -m pytest --cov=lox lox/