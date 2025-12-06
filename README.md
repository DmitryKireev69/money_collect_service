## money_collect_service
# Веб-сервис групповых денежных сборов.

## Быстрый старт / Setup проекта

### 1.Клонировать репозиторий
```
git clone https://github.com/DmitryKireev69/money_collect_service.git
cd money_collect_service
```

### 2. Создать файл переменных окружения
```
В корне проекта есть шаблон:
.env.example
Создайте на его основе рабочий файл .env:
```

### 3. Собрать и запустить контейнеры
```
docker compose up -d --build
После выполнения команда поднимет все
необходимые сервисы и создает бд и применяет миграции на неё.
Так же создан суперпользователь (login:admin, password:admin)
Веб приложение доступно по адресу 127.0.0.1:8000
```

### 4.Генерация моковых данных (seed data)
```
В проекте есть кастомная Django-команда для заполнения базы тестовыми данными.
Команду нужно запускать внутри контейнера backend.
```

### 4.1. Зайти в контейнер:
docker exec -it django_app bash
(Имя контейнера может отличаться — при необходимости проверь через docker ps.)

### 2. Выполнить команду генерации мок-данных:

```
python manage.py seed_data
При выполнении будут созданы:
2000 пользователей
2000 сборов
5000 платежей
```

## Запуск проекта без Docker (локальная разработка)
### Если нужно запустить проект вручную без контейнеров:

```
uv sync
source venv/bin/activate # или venv\Scripts\activate на Windows
cp .env.example .env
в POSTGRES_HOST=db указать localhost

Запуск celery локально
celery -A collect_service.celery worker --loglevel=info -P solo

python manage.py migrate
python manage.py runserver
```

## Полезные команды
```
Логи backend:
    docker logs -f postgres_db
    docker logs -f redis
    docker logs -f django_app
    docker logs -f celery_worker
```


# Перезапуск контейнеров из директории с docker-compose.yml:
```
Перезапуск проекта:
    docker compose restart
Остановка проекта:
    docker compose down```