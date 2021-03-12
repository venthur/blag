# system python interpreter. used only to create virtual environment
PY = python3
VENV = venv

ifeq ($(OS), Windows_NT)
	BIN=$(VENV)/Scripts
	PY=python
else
	BIN=$(VENV)/bin
endif


all: lint test

$(VENV): requirements.txt requirements-dev.txt setup.py
	$(PY) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade -r requirements.txt
	$(BIN)/python -m pip install --upgrade -r requirements-dev.txt
	$(BIN)/python -m pip install -e .
	touch $(VENV)

test: $(VENV)
	$(BIN)/python -m pytest
.PHONY: test

lint: $(VENV)
	$(BIN)/python -m flake8
.PHONY: lint

release: $(VENV)
	$(BIN)/python setup.py sdist bdist_wheel
	$(BIN)/twine upload dist/*
.PHONY: release

clean:
	rm -rf build dist *.egg-info
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	# coverage
	rm -rf htmlcov .coverage
.PHONY: clean
