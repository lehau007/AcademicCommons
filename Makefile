.PHONY: up down seed test test-e2e migrate lint typecheck openapi help

## up          — Build images and start all services in the background
up:
	docker compose up -d --build

## down        — Stop and remove all containers
down:
	docker compose down

## migrate     — Run Alembic DB migrations
migrate:
	cd src/backend && uv run alembic upgrade head

## seed        — Load seed data into the database
seed:
	cd src/backend && uv run python -m app.cli seed

## test        — Run unit tests
test:
	cd src/backend && uv run pytest tests/unit

## test-e2e    — Run end-to-end tests (requires running infra)
test-e2e:
	cd src/backend && RUN_E2E=1 uv run pytest tests/e2e

## lint        — Run ruff linter over app, tests, alembic
lint:
	cd src/backend && uv run ruff check app tests alembic

## typecheck   — Run mypy static type checking
typecheck:
	cd src/backend && uv run mypy app

## openapi     — Export OpenAPI spec to docs/api/openapi.yaml
openapi:
	cd src/backend && uv run python -m app.cli export-openapi --output ../../docs/api/openapi.yaml

## help        — Show this help message
help:
	@grep -E '^## ' Makefile | sed 's/^## /  /'
