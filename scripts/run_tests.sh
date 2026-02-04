#!/bin/bash

# Скрипт для запуска тестов локально (эмуляция CI)

set -e  # Выход при ошибке

echo "🧪 Запуск тестов..."
echo ""

# Проверка наличия pytest в PATH
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest не найден. Устанавливаем зависимости..."
    pip install -r requirements.txt
fi

# Проверка наличия тестовой БД
echo "📦 Проверка тестовой БД..."
if ! psql -lqt | cut -d \| -f 1 | grep -qw skillmap_test; then
    echo "⚠️  База данных skillmap_test не найдена. Создаем..."
    createdb skillmap_test || true
fi

# Установка переменных окружения
export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/skillmap_test"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="skillmap_test"
export DB_USER="user"
export DB_PASSWORD="password"
export APP_ENV="test"
export DEBUG="false"

# Запуск тестов
echo ""
echo "🚀 Запуск pytest..."
pytest -v --cov=src --cov-report=term-missing --cov-report=html

# Результаты
echo ""
if [ $? -eq 0 ]; then
    echo "✅ Все тесты прошли успешно!"
    echo "📊 Отчет о покрытии: htmlcov/index.html"
else
    echo "❌ Тесты провалились"
    exit 1
fi
