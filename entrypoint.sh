#!/bin/sh

echo "Ожидание запуска базы данных..."
while ! nc -z db 5432; do
  sleep 1
done
echo "База данных готова!"

if [ "$1" = "django" ]; then
    echo "Применение миграций..."
    python manage.py migrate --noinput

    echo "Создание суперпользователя..."
    python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Суперпользователь создан.")
else:
    print("Суперпользователь уже существует.")
EOF

    echo "Запуск сервера Django..."
    exec python manage.py runserver 0.0.0.0:8000

elif [ "$1" = "celery" ]; then
    shift
    echo "Запуск Celery воркера..."
    exec celery -A collect_service worker "$@"

else
    echo "Неизвестная команда, выполнение: $@"
    exec "$@"
fi
