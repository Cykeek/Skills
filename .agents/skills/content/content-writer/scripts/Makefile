.PHONY: lint test fix brief ci clean help

PYTHON ?= python
SKILL_DIR := .agents/skills/content-writer
LINTER := $(SKILL_DIR)/lint_content.py
BRIEF := $(SKILL_DIR)/generate_brief.py
REFS := $(SKILL_DIR)/references/*.md
TEMPLATES := $(SKILL_DIR)/templates/*.md
TESTS := $(SKILL_DIR)/tests

help:
	@echo "Content Writer skill targets:"
	@echo "  lint   Run strict content lint on all references and templates"
	@echo "  test   Run pytest if tests exist"
	@echo "  fix    Run linter fixes in-place on all references and templates"
	@echo "  brief  Run the brief generator"
	@echo "  ci     Run lint and test"
	@echo "  clean  Remove generated reports and caches"

lint:
	$(PYTHON) $(LINTER) --strict --json $(REFS) $(TEMPLATES)

test:
	@if [ -d "$(TESTS)" ] && [ "$$(ls -A $(TESTS) 2>/dev/null)" ]; then \
		$(PYTHON) -m pytest $(TESTS) -x; \
	else \
		echo "No tests directory found, skipping tests"; \
	fi

fix:
	$(PYTHON) $(LINTER) --fix --in-place $(REFS) $(TEMPLATES)

brief:
	$(PYTHON) $(BRIEF)

ci: lint test

clean:
	rm -rf .pytest_cache htmlcov .coverage
	rm -f $(SKILL_DIR)/lint_output.json $(SKILL_DIR)/pytest_report.json