.DEFAULT_GOAL := all

.PHONY: .uv
.uv: ## Check that uv is installed
	@uv --version || echo 'Please install uv: https://docs.astral.sh/uv/getting-started/installation/'

.PHONY: install
install: .uv  ## Install the package, dependencies
	uv sync --frozen --all-extras --all-packages

.PHONY: sync
sync: .uv ## Update local packages and uv.lock
	uv sync --all-extras --all-packages

.PHONY: pre-commit
pre-commit: .uv ## Install pre-commit hooks
	@echo "Installing pre-commit hooks"
	@uv run pre-commit install
	
.PHONY: format
format: ## Format the code
	uv run ruff format
	uv run ruff check --fix --fix-only

.PHONY: lint
lint: ## Lint the code
	uv run ruff format --check
	uv run ruff check

.PHONY: typecheck-pyright
typecheck-pyright:
	@# PYRIGHT_PYTHON_IGNORE_WARNINGS avoids the overhead of making a request to github on every invocation
	PYRIGHT_PYTHON_IGNORE_WARNINGS=1 uv run pyright

.PHONY: typecheck
typecheck: typecheck-pyright ## Run static type checking


.PHONY: all
all: format lint typecheck ## Run code formatting, linting, static type checks

