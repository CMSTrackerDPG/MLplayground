#!/bin/bash

python manage.py collectstatic --noinput
# python manage.py migrate --run-syncdb

daphne -b 0.0.0.0 -p 8080 --application-close-timeout 60 mlp.asgi:application
# gunicorn --bind=0.0.0.0:8080 mlp.wsgi
# python manage.py runserver 0.0.0.0:8080
