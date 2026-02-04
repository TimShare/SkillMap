# Contributing to SkillMap

Спасибо за интерес к проекту! 🎉

## 🚀 Быстрый старт

1. **Форкните репозиторий**
   ```bash
   # Клонируйте ваш форк
   git clone https://github.com/YOUR_USERNAME/SkillMap.git
   cd SkillMap
   ```

2. **Создайте виртуальное окружение**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости**
   ```bash
   make install
   # или
   pip install -r requirements.txt
   ```

4. **Создайте тестовую БД**
   ```bash
   make db-create
   # или
   createdb skillmap_test
   ```

5. **Запустите тесты**
   ```bash
   make test
   ```

## 🔄 Процесс разработки

### 1. Создайте новую ветку

```bash
git checkout -b feature/amazing-feature
# или
git checkout -b fix/bug-description
```

Имена веток:
- `feature/` - новая функциональность
- `fix/` - исправление бага
- `docs/` - изменения в документации
- `refactor/` - рефакторинг кода
- `test/` - добавление тестов

### 2. Внесите изменения

Пишите чистый, понятный код следуя принципам проекта:
- Clean Architecture
- SOLID принципы
- Type hints где возможно
- Docstrings для функций и классов

### 3. Добавьте тесты

**Обязательно** добавьте тесты для нового функционала:

```bash
# Unit тесты для бизнес-логики
tests/unit/test_service.py

# Integration тесты для API
tests/integration/test_api.py
```

Минимальное покрытие: **80%**

```bash
# Проверка покрытия
make test
make coverage  # Откроет htmlcov/index.html в браузере
```

### 4. Проверьте код

```bash
# Линтинг
make lint

# Форматирование
make format

# Полная проверка (как в CI)
make ci-test
```

### 5. Закоммитьте изменения

Используйте [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git add .
git commit -m "feat: добавить endpoint для поиска пользователей"
# или
git commit -m "fix: исправить хеширование пароля при обновлении"
# или
git commit -m "test: добавить тесты для UserService.update_user"
```

Типы коммитов:
- `feat:` - новая функциональность
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `test:` - добавление/изменение тестов
- `refactor:` - рефакторинг
- `style:` - форматирование кода
- `chore:` - обновление зависимостей, конфигурации

### 6. Отправьте Pull Request

```bash
git push origin feature/amazing-feature
```

Затем создайте PR на GitHub с описанием:
- Что изменено
- Зачем изменено
- Как протестировано

## ✅ Чеклист перед PR

- [ ] Код проходит все тесты (`make test`)
- [ ] Покрытие тестами >= 80%
- [ ] Линтинг пройден (`make lint`)
- [ ] Код отформатирован (`make format`)
- [ ] Добавлены docstrings
- [ ] Обновлена документация (если нужно)
- [ ] Коммиты следуют Conventional Commits
- [ ] PR описание заполнено

## 🧪 Запуск тестов

```bash
# Все тесты
make test

# Только unit
make test-unit

# Только integration
make test-integration

# С детальным выводом
pytest -v --tb=short

# Конкретный тест
pytest tests/unit/test_service.py::TestUserService::test_create_user -v
```

## 📝 Написание тестов

### Unit тесты

```python
import pytest
from src.service.user import UserService
from src.service.models.user import UserDTO

@pytest.mark.asyncio
async def test_create_user_hashes_password(mock_repository):
    """Тест хеширования пароля при создании пользователя."""
    service = UserService(mock_repository)
    
    user = UserDTO(
        name="Test User",
        email="test@example.com",
        hashed_password="PlainPassword123!"
    )
    
    await service.create_user(user)
    
    # Проверяем что пароль был захеширован
    assert user.hashed_password != "PlainPassword123!"
    assert user.hashed_password.startswith("$2b$")
```

### Integration тесты с канонизацией (snapshots)

```python
import pytest
from syrupy.assertion import SnapshotAssertion

@pytest.mark.asyncio
async def test_get_user_success(
    client: AsyncClient,
    created_user,
    snapshot: SnapshotAssertion
):
    """Тест получения пользователя."""
    response = await client.get(f"/users/{created_user.id}")
    
    assert response.status_code == 200
    
    # Канонизация ответа (snapshot testing)
    data = response.json()
    snapshot_data = {k: v for k, v in data.items() if k != "id"}
    snapshot.assert_match(snapshot_data)
```

## 🏗️ Структура проекта

```
src/
├── app.py                   # FastAPI приложение
├── core/                    # Конфигурация и утилиты
├── interface/               # API слой (routers, schemas)
├── service/                 # Бизнес-логика
├── repository/              # Доступ к данным
└── database/                # ORM модели

tests/
├── conftest.py              # Общие фикстуры
├── unit/                    # Unit тесты
└── integration/             # Integration тесты
    └── __snapshots__/       # Snapshot файлы
```

## 🤝 Code Review

При ревью мы обращаем внимание на:

1. **Архитектура**
   - Соблюдение Clean Architecture
   - Разделение ответственности (SRP)
   - Dependency Injection

2. **Качество кода**
   - Читаемость и понятность
   - Type hints
   - Docstrings
   - Отсутствие code smells

3. **Тесты**
   - Покрытие новой функциональности
   - Качество тестов (не хрупкие, понятные)
   - Snapshot тесты для API

4. **Безопасность**
   - Валидация входных данных
   - Правильное хранение паролей
   - SQL injection защита

## 📞 Вопросы?

- Создайте Issue для обсуждения
- Спросите в Pull Request

Спасибо за ваш вклад! 🙏
