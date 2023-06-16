# system python interpreter. used only to create virtual environment
PY = python3
VENV = venv
BIN=$(VENV)/bin

DOCS_SRC = docs
DOCS_OUT = site


ifeq ($(OS), Windows_NT)
	BIN=$(VENV)/Scripts
	PY=python
endif


.PHONY: all
all: lint mypy test test-release

$(VENV): requirements.txt requirements-dev.txt pyproject.toml
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r requirements.txt
	$(BIN)/pip install --upgrade -r requirements-dev.txt
	$(BIN)/pip install -e .['dev']
	touch $(VENV)

.PHONY: test
test: $(VENV)
	$(BIN)/pytest

.PHONY: mypy
mypy: $(VENV)
	$(BIN)/mypy

.PHONY: lint
lint: $(VENV)
	$(BIN)/flake8

.PHONY: build
build: $(VENV)
	rm -rf dist
	$(BIN)/python3 -m build

.PHONY: test-release
test-release: $(VENV) build
	$(BIN)/twine check dist/*

.PHONY: release
release: $(VENV) build
	$(BIN)/twine upload dist/*

.PHONY: update-pygmentize
update-pygmentize: $(VENV)
	$(BIN)/pygmentize -f html -S default > blag/static/code-light.css
	$(BIN)/pygmentize -f html -S monokai > blag/static/code-dark.css

.PHONY: docs
docs: $(VENV)
	$(BIN)/mkdocs build

.PHONY: clean
clean:
	rm -rf build dist *.egg-info
	rm -rf $(VENV)
	rm -rf $(DOCS_OUT)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	# coverage
	rm -rf htmlcov .coverage
	rm -rf .mypy_cache
