#!/bin/sh
#safe wait until the postgres container is up
sleep 15

python manage.py makemigrations
python manage.py migrate
python manage.py admin_creation
python manage.py exchanges_cache
python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:80 ebury.wsgi:application --access-logfile /logs/gunicorn_access.log --error-logfile /logs/gunicorn_error.log --log-level debug
cd ..
