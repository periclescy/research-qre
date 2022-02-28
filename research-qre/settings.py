"""
Django settings for research-qre project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import socket

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f_t7%*_z&xkfvto8bct1nb_in9uc#$=8311ggocux1sdttw+v4'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
#
# ALLOWED_HOSTS = ['*']

if socket.gethostname() == "server_name":
    DEBUG = False
    ALLOWED_HOSTS = ["example.pericles.cy", ]
    ...
else:
    DEBUG = True
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", ]
    ...

# Application definition

INSTALLED_APPS = [
    'pages.apps.PagesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'import_export',
    'ckeditor',
    'crispy_forms',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'research-qre.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'pages/templates/pages')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'research-qre.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'de8vv077t9dktf',
#         'USER': 'xmefiozizqshvm',
#         'PASSWORD': 'df83cdda32be7fa74042eb676873162b745818c50c8aca31dc1febf90b0a6d0b',
#         'HOST': 'ec2-46-137-84-140.eu-west-1.compute.amazonaws.com',
#         'PORT': '5432',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'research-qre',
#         'USER': 'postgres',
#         'PASSWORD': 'pericles.28',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # Activate Django-Heroku.
# django_heroku.settings(locals())

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/start"
LOGOUT_REDIRECT_URL = "/"

CKEDITOR_CONFIGS = {
    'default': {
        'width': 'auto',
        'autoParagraph': False,
        'htmlEncodeOutput': False,
        'entities': False,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
        ]
    },
    'caption': {
        'height': 80,
        'width': 'auto',
        'autoParagraph': False,
        'htmlEncodeOutput': False,
        'entities': False,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic'],
        ]
    },
    'question': {
        'height': 160,
        'width': 'auto',
        'autoParagraph': False,
        'htmlEncodeOutput': False,
        'entities': False,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic'],
        ]
    },
    'instruction': {
        'height': 300,
        'width': 'auto',
        'autoParagraph': False,
        'htmlEncodeOutput': False,
        'entities': False,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Source', '-', 'Bold', 'Italic', 'Underline'],
        ]
    }
}

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}
