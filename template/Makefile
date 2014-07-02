#_______________________________________________________________________________
#
#                       Makefile
#_______________________________________________________________________________
#

export PYTHONPATH=$(shell echo $(PWD))

PYTHON=python

all: clean docs

clean: clean-pyc clean-docs

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +

docs:
	sphinx-apidoc -o docs apispec/
	@rm -f docs/modules.rst
	sphinx-build -b html docs/ docs/_build/

clean-docs:
	@rm -rf docs/_build/
	@rm -f docs/modules.rst
	@rm -f docs/apispec.*

.PHONY: clean-pyc docs
