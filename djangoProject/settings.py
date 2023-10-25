import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import django
from corsheaders.defaults import default_headers
from django.utils.translation import gettext_lazy as _

from djangoProject import webinar, user, tag

BASE_DIR = Path(__file__).resolve().parent.parent


# SECRET_KEY = os.environ.get("SECRET_KEY")

CORS_ORIGIN_ALLOW_ALL = True

# DEBUG = int(os.environ.get("DEBUG", default=0))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_qf4odh)u1g)3y9g)5sscxp!kz!$mlqz#$)__+6v-f6-y94%n5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# False for production.
USE_LOCAL_DB = False

# run django behind https proxy
# In this tuple, when X-Forwarded-Proto is set to https the request is secure.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")



# determines the base subdirectroy under the main domain for redirecting admin urls.
if DEBUG:
    FORCE_SCRIPT_NAME = ''
else:
    FORCE_SCRIPT_NAME = '/api'


# USE_X_FORWARDED_HOST = True

# default to production list.
ALLOWED_HOSTS =[
    # "*"
    "localhost",
    "127.0.0.1",
    # "[::1]"
    "www.seminar-live.com",
    "www.seminar-live.org"
]

# debug mode list: allowing requests from all hosts.
# if DEBUG:
#     ALLOWED_HOSTS = ["*"]




# Application definition

INSTALLED_APPS = [


    'rest_framework',

    # clear cache. has to precede admin
    'clearcache',

    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework.authtoken',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # task scheduling, yet configured with broker
    'django_q',

    # apps
    'djangoProject.webinar',
    'djangoProject.tag',
    'djangoProject.user',
    'djangoProject.person',
    'djangoProject.webinar_stat',
    'djangoProject.talk',
    'djangoProject.lead',
    'djangoProject.link',
    'djangoProject.speaker',
    'djangoProject.userprofile',
    'djangoProject.profilefilter',
    'djangoProject.report',
    'djangoProject.host',
    'djangoProject.organization',
    'djangoProject.note',
    'djangoProject.submission',
    'djangoProject.sources',
    'djangoProject.taggingrecord',
    'djangoProject.tagrelation',
    'djangoProject.twitterrecord',

    # admin plugins
    'admin_object_actions',
    'django_json_widget',
    'nested_admin',
    'colorfield',
    'rangefilter',

    # ...
    'debug_toolbar',

    #
    'django.contrib.postgres',

    # plugins
    'django_filters',
    'corsheaders',
    'crispy_forms',
    'dj_rest_auth',
    'django_extensions',
    'django.contrib.sites',

    # json rpc_api calls
    'modernrpc',

    # timezone field
    'timezone_field',

    # swagger
    'drf_yasg',


    # auth
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',

    # ckeditor
    'ckeditor',
    'ckeditor_uploader',


    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.douban',

    #  mainly for queueing scrapy
    "django_rq",
]

# enabled timezone awareness
# USE_TZ = True

STATIC_ROOT = 'static/'

CKEDITOR_UPLOAD_PATH = 'ckeditor/uploads/'

# needed for registration handling
SITE_ID=1


# set JSON format as default renderer, thereby disable html view of the api endpoints in production
DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

# allow html view of api enpoints only in debug mode
if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
    'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # eg Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        # 'rest_framework.authentication.SessionAuthentication',  # new
    ],
    'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ),
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    # throttle
    'DEFAULT_THROTTLE_RATES': {
        'anon':'60/min',
        'user':'180/min'
    }
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = None

ADMINS = [('Bo', 'admin@seminar-live.com'), ('no-reply', 'no-reply@seminar-live.com')]


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


# All Auth Settings

# customize allauth adapter for customized email verification url
# Repoint this setting to a subclass of the DefaultAccountAdapter
# so we can override how it handles account verification to allow
# for usage in an SPA context.
ACCOUNT_ADAPTER = 'djangoProject.common.accountadapter.CustomAccountAdapter'

# An email verification URL that the client will pick up.
CUSTOM_ACCOUNT_CONFIRM_EMAIL_URL = "/verify-email/{0}"
CUSTOM_ACCOUNT_RESET_EMAIL_URL = "/password/reset/"

MAIN_DOMAIN_NAME = 'https://www.seminar-live.com'

# AUTH_USER_MODEL='djangoProject.user.CustomizeUser'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS= 1
# whether email verification is required to log in
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# old config for Google domain.
# EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_PASSWORD='iqybbkljnksubgqr'
# EMAIL_HOST_USER='noreply@seminar-live.com'
# EMAIL_PORT = 587

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = _
SERVER_EMAIL = 'no-reply@seminar-live.com'
EMAIL_HOST_PASSWORD = _
EMAIL_USE_SSL = True

# this is aassigned separated from host user because the AWS host user is not human readable. so provide EMAIL FROM in the go
DEFAULT_FROM_EMAIL = 'no-reply@seminar-live.com'

LOGIN_REDIRECT_URL='https://www.seminar-live.com'

MIDDLEWARE = [
    # caching; this must be the firs tmiddle ware
    # 'django.middleware.cache.UpdateCacheMiddleware',

    # put cors first
    'corsheaders.middleware.CorsMiddleware',

    # debug
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # common middle ware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # locale middle ware
    'django.middleware.locale.LocaleMiddleware',

    # common middleware
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # admin middleware
    'crum.CurrentRequestUserMiddleware',

    # django debug middleware
    # 'debug_toolbar.midleware.DebugToolbarMiddleware',



    # fetch from cached, this must be the last middleware
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

CSRF_COOKIE_NAME = "csrftoken"

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200"
]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'Cache-Control',
    "expires",
    "pragma"
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# debugging requests
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'djangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases



# Local development db. Pull up in docker-compose.

if USE_LOCAL_DB:
    DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'sl2',
    'USER': 'sl2',
    'PASSWORD': 'sl2',
    'HOST': 'localhost',
    'PORT': '8003',
    }
}
else:
    DATABASES = {

        # sql db: no longer usable because of the it doesn't allow JSON field
        # 'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': BASE_DIR / 'db.sqlite3',
        # }

        # production db
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',  # aws rds defaults to postgres database
            'USER': 'sl2',  # aws master user name
            # endpoint, needs to be publicly accessible
            'PORT': '5432',
        }

    }

# aws pg S4KALypi0SGpCRUCmZCB

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

OLD_PASSWORD_FIELD_ENABLED = True # to use old_password when resetting password.
LOGOUT_ON_PASSWORD_CHANGE = False #to keep the user logged in after password change

# rest template
REST_AUTH_SERIALIZERS = {
    # 'PASSWORD_RESET_SERIALIZER': 'djangoProject.user.auth_serializers.MyPasswordResetSerializer'
}

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# multilanguage setting for parler


LANGUAGES = (
    ('en-us', _("English")),
    ('cn', _("Chinese"))
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# amazon s3 settings

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

AWS_STORAGE_BUCKET_NAME = 'seminarlive'

AWS_ACCESS_KEY_ID='AKIASZPQAT32ZWDBKDSO'

AWS_SECRET_ACCESS_KEY='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'


# AWS_DEFAULT_ACL = 'public-read'

# prevent generated url to contain query strings such as my aws key.
AWS_QUERYSTRING_AUTH = False

# make objects public
AWS_S3_BUCKET_AUTH = False
# let objects expire after a while
AWS_S3_MAX_AGE_SECONDS = 60 * 60 * 24 * 365  # 1 year.

# amazon signiture version, needed for queryey string url to uploaded file
AWS_S3_SIGNATURE_VERSION = 's3v4'

AWS_S3_REGION_NAME = 'ap-northeast-2'

# fixes the Amazon s3. signiture error
AWS_S3_ADDRESSING_STYLE = "virtual"

# RPC API methods
MODERNRPC_METHODS_MODULES = [
    'rpc_api.rpc_methods',
    'scraping_center.scrapy_project.scrape_methods'
]

if DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://localhost:8004",
            "TIMEOUT": None,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": "redis_secret",
                "IGNORE_EXCEPTIONS": True,
            }
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": "redis_secret",
                "IGNORE_EXCEPTIONS": True,
            }
        }
    }


CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = '60'
CACHE_MIDDLEWARE_KEY_PREFIX = 'sl2'

# Use redis as the default backen engine for session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

RQ_QUEUES = {
    'default':
        {
        'USE_REDIS_CACHE': 'default',
    },
}
# redis qr

# RQ_QUEUES = {
#     'default': {
#         'HOST': 'localhost',
#         'PORT': 6379,
#         'DB': 0,
#         'PASSWORD': 'redis',
#         'DEFAULT_TIMEOUT': 360,
#     },
#     'with-sentinel': {
#         'SENTINELS': [('localhost', 26736), ('localhost', 26737)],
#         'MASTER_NAME': 'redismaster',
#         'DB': 0,
#         'PASSWORD': 'secret',
#         'SOCKET_TIMEOUT': None,
#         'CONNECTION_KWARGS': {
#             'socket_connect_timeout': 0.3
#         },
#     },
#     'high': {
#         'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'), # If you're on Heroku
#         'DEFAULT_TIMEOUT': 500,
#     },
#     'low': {
#         'HOST': 'localhost',
#         'PORT': 6379,
#         'DB': 0,
#     }
# }

# RQ_EXCEPTION_HANDLERS = ['path.to.my.handler'] # If you need custom exception handlers

# this increase db quert efficiency when the same user makes multiple queries within 300 seconds.
CONN_MAX_AGE=60

#rq logging
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "rq_console": {
#             "format": "%(asctime)s %(message)s",
#             "datefmt": "%H:%M:%S",
#         },
#     },
#     "handlers": {
#         "rq_console": {
#             "level": "DEBUG",
#             "class": "rq.utils.ColorizingStreamHandler",
#             "formatter": "rq_console",
#             "exclude": ["%(asctime)s"],
#         },
#         # If you use sentry for logging
#     #     'sentry': {
#     #         'level': 'ERROR',
#     #         'class': 'raven.contrib.django.handlers.SentryHandler',
#     #     },
#     },
#     'loggers': {
#         "rq.worker": {
#             "handlers": ["rq_console"],
#             "level": "ERROR"
#         },
#     }
# }

# JSON EDITOR STATIC FILES
# https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.1.9/jsoneditor.min.js

JSON_EDITOR_JS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.1.9/jsoneditor.min.js'
JSON_EDITOR_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.1.9/jsoneditor.min.css'

# flush redis when debugging
from django_redis import get_redis_connection
if DEBUG:
    def tearDown():
        get_redis_connection("default").flushall()

    tearDown()
