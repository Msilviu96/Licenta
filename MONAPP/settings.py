"""
Django settings for MONAPP project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@(u%6+(wf_e_8*n-ys)vx8w4(dhz!*vdgx#xo=69lzxbu!yg^m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'MONAPP\media')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'database',
    'map',
    'child',
    'rest_api',
    'leaflet',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MONAPP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'MONAPP.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

SESSION_USER_ID_FIELD_NAME = 'parent_id'

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (47.155, 27.60),
    'DEFAULT_ZOOM': 14,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 20,
    'SCALE': 'both',
    'PLUGINS': {
        'name-of-plugin': {
            'css': 'https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.4.2/leaflet.draw.css',
            'js': 'https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.4.2/leaflet.draw.js',
            'auto-include': True,
        },
    },
    'TILES': [
        ('Streets', 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
         {'attribution': '&copy; Big eye', 'maxZoom': 20, 'subdomains': ['mt0', 'mt1', 'mt2', 'mt3']}),
        ('Hybrid', 'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',
         {'attribution': '&copy; Big eye', 'maxZoom': 20, 'subdomains': ['mt0', 'mt1', 'mt2', 'mt3']}),
        ('Satellite', 'http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
         {'attribution': '&copy; Big eye', 'maxZoom': 20, 'subdomains': ['mt0', 'mt1', 'mt2', 'mt3']}),
    ]
}

if __name__ == '__main__':
    apps_database = [
        {'name': 'app_1', 'blocked': "N"},
        {'name': 'app_2', 'blocked': "Y"},
        {'name': 'app_3', 'blocked': "Y"},
    ]

    apps_received = [
        {'name': 'app_1', 'blocked': "N"},
        {'name': 'app_2', 'blocked': "N"},
        {'name': 'app_4', 'blocked': 'N'}
    ]

    apps_received = sorted(apps_received, key=lambda k: k['name'])

    apps_toSave = list()

    comparatii = 0
    flag_append = False

    for i in range(len(apps_received)):
        for j in range(len(apps_database)):
            flag_append = True
            comparatii += 1
            if apps_received[i]['name'] == apps_database[j]['name']:
                apps_toSave.append({
                    'name': apps_database[j]['name'],
                    'blocked': apps_database[j]['blocked']
                })
                flag_append = False
                break
            elif apps_received[i]['name'][0] > apps_database[j]['name'][0]:
                apps_toSave.append({
                    'name': apps_received[i]['name'],
                    'blocked': apps_received[i]['blocked']
                })
                flag_append = False
                break
        if flag_append:
            apps_toSave.append({
                'name': apps_received[i]['name'],
                'blocked': apps_received[i]['blocked']
            })

    for app_toSave in apps_toSave:
        print(app_toSave)

    print(comparatii)
