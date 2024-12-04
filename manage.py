"""Django's command-line utility for administrative tasks."""
import os
import sys
# import environ
from dotenv import load_dotenv

def main():
    """Run administrative tasks."""
    
    # Charger le fichier .env
    load_dotenv()

    # Déterminer l'environnement (par exemple, "prod" ou "dev")
    environment = os.getenv('DJANGO_ENV', 'dev')

    # Basculer entre les configurations selon l'environnement
    # Définir explicitement la variable d'environnement DJANGO_SETTINGS_MODULE
    if environment == 'prod':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'blog_project.settings'
    else:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'blog_project.dev'

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
