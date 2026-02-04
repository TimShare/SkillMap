# SkillMap API

[![Tests](https://github.com/YOUR_USERNAME/SkillMap/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/SkillMap/actions/workflows/tests.yml)
[![Lint](https://github.com/YOUR_USERNAME/SkillMap/actions/workflows/lint.yml/badge.svg)](https://github.com/YOUR_USERNAME/SkillMap/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/SkillMap/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/SkillMap)

REST API для управления пользователями с использованием FastAPI, PostgreSQL и SQLAlchemy.

## 🚀 Функционал

- ✅ CRUD операции для пользователей
- ✅ Хеширование паролей (bcrypt)
- ✅ Async/await поддержка
- ✅ Clean Architecture (Repository + Service + Router)
- ✅ Миграции БД (Alembic)
- ✅ Docker Compose для разработки
- ✅ Комплексное тестирование (86% покрытие)
- ✅ CI/CD через GitHub Actions

## 📋 Требования

- Python 3.9+
- PostgreSQL 15+
- Docker & Docker Compose (опционально)

## 🛠️ Установка

### С Docker

```bash
# Клонируем репозиторий
git clone https://github.com/YOUR_USERNAME/SkillMap.git
cd SkillMap

# Запускаем контейнеры
docker-compose up --build
```

API будет доступен по адресу: http://localhost:8000

### Без Docker

```bash
# Клонируем репозиторий
git clone https://github.com/YOUR_USERNAME/SkillMap.git
cd SkillMap

# Создаем виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate  # Windows

# Устанавливаем зависимости
pip install -r requirements.txt

# Создаем БД
createdb skillmap

# Применяем миграции
alembic upgrade head

# Запускаем сервер
uvicorn src.app:app --reload
```

## 🧪 Тестирование

```bash
# Устанавливаем тестовые зависимости (уже в requirements.txt)
pip install pytest pytest-asyncio pytest-cov syrupy

# Создаем тестовую БД
createdb skillmap_test

# Запускаем тесты
pytest -v

# С покрытием
pytest -v --cov=src --cov-report=html

# Только unit тесты
pytest tests/unit/ -v

# Только integration тесты
pytest tests/integration/ -v
```

### Структура тестов

```
tests/
├── conftest.py              # Фикстуры и настройки
├── unit/                    # Unit тесты
│   ├── test_repository.py   # Тесты слоя данных
│   ├── test_security.py     # Тесты хеширования
│   └── test_service.py      # Тесты бизнес-логики
└── integration/             # Интеграционные тесты
    ├── test_api.py          # Тесты API endpoints
    └── __snapshots__/       # Snapshot тесты (syrupy)
```

**Покрытие:** 86% (256 строк, 36 пропущено)
- Service: 96%
- Security: 100%
- Repository: 71%
- Router: 69%

## 📚 API Документация

После запуска сервера документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Основные эндпоинты

```
POST   /users/          - Создать пользователя
GET    /users/{id}      - Получить пользователя
PUT    /users/{id}      - Обновить пользователя
DELETE /users/{id}      - Деактивировать пользователя
```

## 🏗️ Архитектура

Проект следует принципам Clean Architecture:

```
src/
├── app.py                   # FastAPI приложение
├── core/                    # Ядро приложения
│   ├── database.py          # Конфигурация БД
│   ├── di.py                # Dependency Injection
│   ├── exceptions.py        # Кастомные исключения
│   ├── security.py          # Хеширование паролей
│   └── settings.py          # Настройки приложения
├── interface/               # Слой представления
│   ├── routers/             # FastAPI роутеры
│   └── schemas/             # Pydantic схемы
├── service/                 # Бизнес-логика
│   ├── user.py              # UserService
│   └── models/              # DTO модели
├── repository/              # Слой данных
│   ├── user.py              # UserRepository
│   └── interfaces/          # Интерфейсы репозиториев
└── database/                # ORM модели
    └── models/              # SQLAlchemy модели
```

## 🔧 Конфигурация

Создайте `.env` файл в корне проекта:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/skillmap
DB_HOST=localhost
DB_PORT=5432
DB_NAME=skillmap
DB_USER=user
DB_PASSWORD=password

# Application
APP_ENV=development
DEBUG=true
```

## 🚀 CI/CD

Проект использует GitHub Actions для автоматизации:

### Workflows

1. **Tests** (`.github/workflows/tests.yml`)
   - Запускается при push/PR в main/develop
   - Поднимает PostgreSQL в контейнере
   - Запускает pytest с coverage
   - Отправляет результаты в Codecov

2. **Lint** (`.github/workflows/lint.yml`)
   - Проверяет код с помощью ruff
   - Проверяет типы с помощью mypy

### Настройка для вашего репозитория

1. Замените `YOUR_USERNAME` в README.md на ваш GitHub username
2. (Опционально) Зарегистрируйтесь на [Codecov](https://codecov.io) и добавьте `CODECOV_TOKEN` в GitHub Secrets

## 📝 Миграции

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "описание изменений"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Посмотреть историю
alembic history
```

## 🤝 Разработка

1. Форкните репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

### Code Style

- Используем ruff для линтинга
- Используем mypy для проверки типов
- Минимальное покрытие тестами: 80%

## 📄 Лицензия

Этот проект создан в образовательных целях.

## 👤 Автор

Создано с ❤️ для изучения FastAPI, SQLAlchemy и Clean Architecture
