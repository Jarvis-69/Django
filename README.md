python -m venv env
env\Scripts\activate
pip install pillow
pip install django
python.exe -m pip install --upgrade pip
django-admin startproject blog_project
cd blog_project
python manage.py startapp blog
python manage.py runserver
pip install psycopg2-binary python-dotenv
django-admin startproject monprojet
python manage.py makemigrations
pip install psycopg2
pip install django-environ

# Pour développement
DJANGO_ENV=development python manage.py runserver

# Pour production
DJANGO_ENV=production python manage.py runserver
