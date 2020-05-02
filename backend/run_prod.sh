#!/bin/sh
export DJANGO_SETTINGS=prod
touch /app/log/malamatura.log
touch /app/log/uwsgi.log
cd /app
python3 manage.py migrate
uwsgi --ini /app/config/uwsgi-prod.ini
