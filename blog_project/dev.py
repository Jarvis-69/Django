import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
import environ
 
# Chargement des variables d'environnement depuis .env
load_dotenv()
 
# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent
 
# Paramètres de sécurité
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']  # En production, spécifiez vos domaines
 
# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',  # Notre application blog
    'modeltranslation',
]
 
# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]
 
# Configuration des URLs
ROOT_URLCONF = 'blog_project.urls'
 
# Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Utilisation du moteur de templates Django
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Répertoire des templates si tu en as
        'APP_DIRS': True,  # Recherche de templates dans les répertoires des applications Django
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Outils de debug pour les templates
                'django.template.context_processors.request',  # Informations sur la requête
                'django.contrib.auth.context_processors.auth',  # Gestion de l'authentification
                'django.contrib.messages.context_processors.messages',  # Messages de Django
            ],
        },
    },
]
 
# Configuration WSGI
WSGI_APPLICATION = 'blog_project.wsgi.application'

# Initialise l'environnement
env = environ.Env()
# Lire les variables d'environnement à partir du fichier .env
environ.Env.read_env()

# Configuration de la base de données PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prod',
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}
 
# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),  # Chemin vers le dossier des traductions
]

# Internationalisation
LANGUAGES = [
    ('fr', _('French')),
    ('en', _('English')),
    # autres langues possibles
]

LANGUAGE_SESSION_KEY = 'django_language'  # La clé par défaut pour stocker la langue dans la session

LANGUAGE_CODE = 'fr'  # Par défaut, la langue de l'application sera le français
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
 
# Fichiers statiques (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
 
# Configuration des médias (fichiers uploadés)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
 
# Configuration par défaut des clés primaires
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
 
# Configuration de la redirection après login/logout
LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'blog-home'
 
# Configurations email (à configurer pour la production)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Pour le développement
"""
# Pour la production, utilisez ces paramètres :
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
"""
 
# Configurations de sécurité supplémentaires pour la production
if not DEBUG:
    # HTTPS settings
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
