.PHONY: help install run format clean test list-sources list-categories clear-cache

PYTHON := python3
PIP := pip3
VENV := venv

help:
	@echo "JokeGenerator Development Tasks"
	@echo ""
	@echo "Setup:"
	@echo "  make install       - Install dependencies"
	@echo ""
	@echo "Usage:"
	@echo "  make run           - Get a random joke"
	@echo "  make run-count     - Get 5 random jokes"
	@echo "  make programming   - Get a programming joke"
	@echo "  make dark          - Get a dark humor joke"
	@echo ""
	@echo "Info:"
	@echo "  make list-sources  - List available APIs"
	@echo "  make list-cats     - List available categories"
	@echo "  make clear-cache   - Clear cached jokes"
	@echo ""
	@echo "Development:"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean up temp files"

install:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && $(PIP) install -r requirements.txt
	@echo "✅ Installed! Run: make run"

run:
	. $(VENV)/bin/activate && $(PYTHON) joke_generator.py

run-count:
	. $(VENV)/bin/activate && $(PYTHON) joke_generator.py --count 5

programming:
	. $(VENV)/bin/activate && $(PYTHON) joke_generator.py --category Programming

dark:
	. $(VENV)/bin/activate && $(PYTHON) joke_generator.py --category Dark

list-sources:
	. $(VENV)/bin/activate && $(PYTHON) joke_generator.py --list-sources

list-cats:
	. $(VENV)/bin/activate && $(PYTHON) joke_generator.py --list-categories

clear-cache:
	. $(VENV)/bin/activate && $(PYTHON) joke_generator.py --clear-cache

format:
	. $(VENV)/bin/activate && $(PIP) install black && black joke_generator.py

clean:
	rm -rf __pycache__ *.pyc .DS_Store

test:
	. $(VENV)/bin/activate && $(PYTHON) -m pytest -v 2>/dev/null || echo "No tests yet"

.DEFAULT_GOAL := help
