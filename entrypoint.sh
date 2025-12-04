#!/bin/sh

echo "Waiting for DB..."
while ! nc -z db 5432; do
  sleep 1
done
echo "DB is ready!"

python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
