#!/bin/bash

echo "run makemigrations"
/usr/local/bin/python manage.py makemigrations --no-input

echo "run migrate"
/usr/local/bin/python manage.py migrate --no-input

echo "run collectstatic"
/usr/local/bin/python manage.py collectstatic --no-input

echo "run gunicorn"
RUN_PORT=${PORT-:8004}
/usr/local/bin/gunicorn webecogestion.wsgi:application --bind "0.0.0.0:${RUN_PORT}" --timeout 120 --access-logfile - --error-logfile -
