echo 'Apply database migrations'
python manage.py makemigrations
python manage.py migrate

echo 'start run server'
python manage.py runserver 0.0.0.0:8000