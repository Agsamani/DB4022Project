@echo off

python -m pip install -r requirements.txt

psql -U postgres -f "SqlScripts/init.sql"

python manage.py makemigrations
python manage.py migrate

python elastic.py