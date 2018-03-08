#!/usr/bin/env bash

# check if db is available
until nc -z postgres 5432; do
    echo "$(date) - waiting for postgres..."
    sleep 5
done

# change dir
cd %APP_NAME%

# make & apply migrations
python manage.py makemigrations && python manage.py migrate

# start app
gunicorn %APP_NAME%.wsgi:application -w 2 -b :8000
