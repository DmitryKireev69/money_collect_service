#!/bin/sh

echo "Waiting for DB..."
while ! nc -z db 5432; do
  sleep 1
done
echo "DB is ready!"

# --- Запуск для Django ---
if [ "$1" = "django" ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput

    echo "Creating superuser..."
    python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF

    echo "Starting Django server..."
    exec python manage.py runserver 0.0.0.0:8000

# --- Запуск для Celery ---
elif [ "$1" = "celery" ]; then
    shift
    echo "Starting Celery worker..."
    exec celery -A collect_service worker "$@"

# --- Любая другая команда ---
else
    echo "Unknown command, executing: $@"
    exec "$@"
fi
