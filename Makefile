.PHONY: help install test test-unit test-integration coverage lint format clean docker-up docker-down

help:  ## Показать это сообщение
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Установить зависимости
	pip install -r requirements.txt

test:  ## Запустить все тесты
	export PATH="$$HOME/Library/Python/3.9/bin:$$PATH" && pytest -v --cov=src --cov-report=term-missing --cov-report=html

test-unit:  ## Запустить только unit тесты
	export PATH="$$HOME/Library/Python/3.9/bin:$$PATH" && pytest tests/unit/ -v

test-integration:  ## Запустить только integration тесты
	export PATH="$$HOME/Library/Python/3.9/bin:$$PATH" && pytest tests/integration/ -v

test-watch:  ## Запустить тесты в watch режиме
	export PATH="$$HOME/Library/Python/3.9/bin:$$PATH" && pytest-watch tests/ -v

coverage:  ## Посмотреть coverage в браузере
	open htmlcov/index.html

lint:  ## Проверить код линтером
	ruff check src/ tests/ || true
	mypy src/ --ignore-missing-imports || true

format:  ## Отформатировать код
	ruff check --fix src/ tests/ || true
	ruff format src/ tests/ || true

clean:  ## Очистить временные файлы
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf .pytest_cache htmlcov .coverage coverage.xml

docker-up:  ## Запустить Docker Compose
	docker-compose up --build

docker-down:  ## Остановить Docker Compose
	docker-compose down

db-create:  ## Создать тестовую базу данных
	createdb skillmap_test || echo "База уже существует"

db-migrate:  ## Применить миграции
	alembic upgrade head

db-rollback:  ## Откатить последнюю миграцию
	alembic downgrade -1

dev:  ## Запустить сервер в dev режиме
	uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

ci-test:  ## Эмуляция CI (как в GitHub Actions)
	./scripts/run_tests.sh
