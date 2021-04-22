#!/bin/sh

# Collect static files
pipenv run python manage.py collectstatic --no-input

# Migrate database
pipenv run python manage.py createcachetable
pipenv run python manage.py migrate

# Start Gunicorn application
pipenv run gunicorn transgenderwachttijd.wsgi --bind 0.0.0.0:3000 --forwarded-allow-ips '*' --workers 2 --access-logfile '-'
