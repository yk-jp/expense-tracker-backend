echo 'Apply database migrations'
python manage.py makemigrations
python manage.py migrate

echo 'start run server'
gunicorn core.wsgi --bind 0.0.0.0:8000