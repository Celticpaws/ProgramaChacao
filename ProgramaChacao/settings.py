"""
Django settings for ProgramaChacao project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_zl3r05wez$6r@ip!i$wk9&@0b7&z%n78k!9m%hiay=bjdfk6$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','programachacao.pythonanywhere.com']

IMPORT_EXPORT_USE_TRANSACTIONS = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maximas',
    'core',
    'import_export',
]

SITE_ID = 1

ROOT_URLCONF = "urls"

DEBUG = True

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ),
        },
    },
]

if os.environ.get('IMPORT_EXPORT_TEST_TYPE') == 'mysql-innodb':
    IMPORT_EXPORT_USE_TRANSACTIONS = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'TEST_NAME': 'import_export_test',
            'USER': os.environ.get('IMPORT_EXPORT_MYSQL_USER', 'root'),
            'OPTIONS': {
               'init_command': 'SET storage_engine=INNODB',
            }
        }
    }
elif os.environ.get('IMPORT_EXPORT_TEST_TYPE') == 'postgres':
    IMPORT_EXPORT_USE_TRANSACTIONS = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'import_export',
            'USER': os.environ.get('IMPORT_EXPORT_POSTGRESQL_USER'),
            'PASSWORD': os.environ.get('IMPORT_EXPORT_POSTGRESQL_PASSWORD'),
            'HOST': 'localhost',
            'PORT': 5432
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(__file__), 'database.db'),
        }
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.NullHandler'
        }
    },
    'root': {
        'handlers': ['console'],
    }}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_REDIRECT_URL ='/'
LOGOUT_REDIRECT_URL ='/'
LOGIN_URL=''
