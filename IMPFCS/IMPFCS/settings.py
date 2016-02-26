"""
Django settings for IMPFCS project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!lo5w32f_jn&_w#(w@du8cmpm*6i#_2crdv%9ho02u$wxbe6og'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend',
)

AUTHENTICATION_BACKENDS = ('frontend.authBackend.THUAuthBackend',)

LOGIN_URL = '/site/login'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'IMPFCS.urls'

WSGI_APPLICATION = 'IMPFCS.wsgi.application'
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#SESSION_ENGINE = 'mongoengine.django.sessions'
#SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}

#import json
#config = json.load(open('config.json'))
#MONGO_DATABASE_NAME = config['database_name'] 
#MONGO_HOST = config['database_host']
#MONGO_PORT = config['database_port']
#MONGO_USERNAME = config['database_username']
#MONGO_PASSWORD = config['database_password']
#import mongoengine
#mongoengine.connect(MONGO_DATABASE_NAME, host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USERNAME, password=MONGO_PASSWORD)


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
