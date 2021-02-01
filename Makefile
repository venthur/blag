VENV = venv


all: lint test

$(VENV): requirements.txt requirements-dev.txt setup.py
	python3 -m venv $(VENV)
	$(VENV)/bin/python3 -m pip install --upgrade -r requirements.txt
	$(VENV)/bin/python3 -m pip install --upgrade -r requirements-dev.txt
	$(VENV)/bin/python3 -m pip install -e .
	touch $(VENV)

test: $(VENV)
	$(VENV)/bin/python3 -m pytest
.PHONY: test

lint: $(VENV)
	$(VENV)/bin/python3 -m flake8
.PHONY: lint

release: $(VENV)
	$(VENV)/bin/python3 setup.py sdist bdist_wheel
	$(VENV)/bin/twine upload dist/*
.PHONY: release

clean:
	rm -rf build dist *.egg-info
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	# coverage
	rm -rf htmlcov .coverage
.PHONY: clean
