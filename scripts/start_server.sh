#!/bin/sh

# Change to root directory
cd ..

# Compile translation messages
poetry run python manage.py compilemessages

# Collect static files
poetry run python manage.py collectstatic --no-input

# Migrate database
poetry run python manage.py createcachetable
poetry run python manage.py migrate

# Start Gunicorn application
poetry run gunicorn application.wsgi --bind 0.0.0.0:3000 --forwarded-allow-ips '*' --workers 2 --access-logfile '-'
