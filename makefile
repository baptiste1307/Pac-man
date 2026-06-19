PYTHON = python3
WHL_FILE = mazegenerator-00001-py3-none-any.whl
MAIN = pac-man.py
CONFIG = config.json
RM = rm -rf
SYNC = uv sync
RUN= uv run


install:
	$(SYNC)
	unzip $(WHL_FILE)
	
run:
	PYTHONDONTWRITEBYTECODE=1 $(RUN) $(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb

clean:
	find . -depth -type d -name "__pycache__" -exec $(RM) {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -depth -type d -name "*.egg-info" -exec $(RM) {} + 2>/dev/null || true
	$(RM) .mypy_cache
	$(RM) .pytest_cache
	$(RM) venv
	$(RM) .venv
	$(RM) data/output

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . \
		--warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

.PHONY: install run debug test clean lint lint-strict