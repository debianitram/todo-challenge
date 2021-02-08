import sys

import environ
from django.utils.translation import gettext_lazy as _


ROOT_DIR = environ.Path(__file__) - 3
PROJECT_DIR = ROOT_DIR.path('project')
APPS_DIR = PROJECT_DIR.path('apps')

sys.path.insert(0, str(APPS_DIR))

# Load operating system environment variables and then prepare to use them
env = environ.Env()
#  patch for https://github.com/joke2k/django-environ/issues/119
env_file = str(ROOT_DIR.path('.env'))
env.read_env(env_file)

# PROJECT
PROJECT_NAME_HEADER = env('PROJECT_NAME_HEADER', default='Project Name')
PROJECT_NAME_TITLE = env('PROJECT_NAME_TITLE', default='Project Name')

SECRET_KEY = env('DJANGO_SECRET_KEY', default='CHANGEME!!!')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default='*')       # noqa

DATABASES = {
    'default': env.db('DATABASE_URL')
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'django_filters',
)

PROJECT_APPS = (
    'todo',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('es', _('Spanish')),
]

LOCALE_PATHS = [str(PROJECT_DIR.path('translations'))]


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = str(PROJECT_DIR.path('static'))
STATIC_URL = env.str('DJANGO_STATIC_URL', default='/static/')

MEDIA_ROOT = str(PROJECT_DIR.path('media'))
MEDIA_URL = env.str('DJANGO_MEDIA_URL', default='/media/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(PROJECT_DIR.path('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGOUT_REDIRECT_URL = '/'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

if DEBUG:
    INSTALLED_APPS += ('django_extensions', )
