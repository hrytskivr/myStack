#!/bin/sh

# check if db is available, if no - container exits with code 1,
# regulated by 'restart_policy' in 'docker-stack.yml'
until nc -z %DB_ADDRESS% %DB_PORT%; do
    echo "$(date) - waiting for database..."
    exit 1
done

# change dir into app folder
cd %APP_NAME%

# make & apply migrations
python manage.py makemigrations && python manage.py migrate

# run application
gunicorn %APP_NAME%.wsgi:application -b :8000
