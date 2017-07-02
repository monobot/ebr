import os

_ = lambda s: s


SECRET_KEY = '6(pfod42bhw23s^=i6#pc3r8*gz7d_cd7frq-n-pg#auu)$v(d'

#     PATH CONFIGURATION
BASE_DIR = os.path.abspath(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

SITE_NAME = os.path.basename(BASE_DIR)
#     END PATH CONFIGURATION

#     DEBUG CONFIGURATION
# Disable debugging by default.
TESTING = False

DEBUG = True
#     END DEBUG CONFIGURATION

#     MANAGER CONFIGURATION
# Admin and managers for this project. These people receive private site
# alerts.
ADMINS = (('monobot', 'monobot.soft@gmail.com'), )

MANAGERS = ADMINS
#     END MANAGER CONFIGURATION

#     GENERAL CONFIGURATION
ALLOWED_HOSTS = [
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
    'django',
]

TIME_ZONE = 'UTC'
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html.

SITE_ID = 1

#     LOCALIZATION CONFIGURATION
LANGUAGE_CODE = 'en-EN'

USE_I18N = True

USE_L10N = True

LANGUAGES = (
    ('en', _('English')),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )
#     END LOCALIZATION CONFIGURATION

SECURE_REQUIRED_PATHS = ('/media/', '/static/')

WSGI_APPLICATION = 'ebury.wsgi.application'

LOGIN_URL = '/usuario/login/'
LOGIN_REDIRECT_URL = '/'

MAX_UPLOAD_SIZE = '10485760'
#     END GENERAL CONFIGURATION

#     CACHE CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis_cache:6379',
    },
}
#     END CACHE CONFIGURATION

#     DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db_eb_postgres',
        'PORT': '5432',
    },
    'testing': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db_eb_testing',
        'PORT': '5432',
    },
}
#     END DATABASE CONFIGURATION

#     TEMPLATES CONFIGURATION
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
#     END TEMPLATES CONFIGURATION

#     MEDIA CONFIGURATION
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'
#     END MEDIA CONFIGURATION

#     STATIC FILE CONFIGURATION
# Absolute path to the directory static files should be collected to. Don't put
# anything in this directory yourself; store your static files in apps' static/
# subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
ADMIN_MEDIA_PREFIX = '/static/admin/'

#     END STATIC FILE CONFIGURATION

#     MIDDLEWARE CONFIGURATION
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#     END MIDDLEWARE CONFIGURATION

#     APP CONFIGURATION
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # installed apps
    'bootstrapform',
    'rest_framework',

    # local apps
    'currency.apps.CurrencyConfig',
]
#     END APP CONFIGURATION

#     PASSWORD_VALIDATORS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.'
             'UserAttributeSimilarityValidator'
     },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
     },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
     },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
     },
]
#     END PASSWORD_VALIDATORS

#     URL LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'normal': {
            'format': '%(asctime)s %(name)s - %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'ebury_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10485760,  # 10 megas filesize
            'backupCount': 2,  # maximo dos copias backup
            'filename': '/logs/django.log',
            'formatter': 'normal'
        },
    },
    'loggers': {
        'ebury': {
            'handlers': ['ebury_handler'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}
#     END CACHE LOGGING

#     URL CONFIGURATION
ROOT_URLCONF = 'ebury.urls'
#     END URL CONFIGURATION

#     SPECIFIC CONFIGURATION
GROUP_OWNER = 'owner'
GROUP_MEMBER = 'member'

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ['localhost', ]
#     END SPECIFIC CONFIGURATION
