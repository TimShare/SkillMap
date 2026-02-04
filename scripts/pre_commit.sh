#!/bin/bash

# Скрипт для проверки кода перед коммитом (pre-commit hook)

set -e

echo "🔍 Проверка кода..."
echo ""

# Форматирование и линтинг (если установлен ruff)
if command -v ruff &> /dev/null; then
    echo "📝 Проверка с ruff..."
    ruff check src/ tests/ || true
fi

# Проверка типов (если установлен mypy)
if command -v mypy &> /dev/null; then
    echo "🔬 Проверка типов с mypy..."
    mypy src/ --ignore-missing-imports || true
fi

# Запуск быстрых unit тестов
echo ""
echo "🧪 Запуск unit тестов..."
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
pytest tests/unit/ -v --tb=short

echo ""
echo "✅ Pre-commit проверки завершены!"
