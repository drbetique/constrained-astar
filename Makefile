PY?=python3
PIP?=pip3

.PHONY: venv install run lint fmt

venv:
	$(PY) -m venv .venv
	. .venv/bin/activate && $(PIP) install -U pip

install:
	. .venv/bin/activate && $(PIP) install -r requirements.txt

run:
	. .venv/bin/activate && $(PY) -m email_to_sheets.main --dry-run
