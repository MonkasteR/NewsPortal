"""
Django settings for NewsPortal project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%o29qkzfg!g_l=*5t0h=m=^#nzc1b!n)xq1)(j8#atqfo51@#p'

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['localhost', '127.0.0.1']

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'News.apps.NewsConfig',
    'django.contrib.sites',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'NewsPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'News.context_processors.news_for_header',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewsPortal.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/news"
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"
ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomSignupForm'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True

SITE_URL = 'http://127.0.0.1:8000'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
load_dotenv()
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

APSCHEDULER_DATEFORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

BROCKER_URL = os.getenv("BROCKER_URL")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_ALWAYS_EAGER = True
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": "redis://localhost:6379",
#     }
# }

DEBUG = True

logger = logging.getLogger(__name__)
''' Ниже код для установки цветного вывода логов, удобно для консоли '''
# handler = colorlog.StreamHandler()
# handler.setFormatter(
#     colorlog.ColoredFormatter(
#         '%(log_color)s%(asctime)s %(levelname)s %(name)s %(message)s'
#     )
# )
#
# logger = colorlog.getLogger(__name__)
# logger.addHandler(handler)

# Устанавливаем путь к каталогу для хранения логов
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')

# Создаем каталог для хранения логов, если его нет
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'console_filter': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'file_email_filter': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'console_formatter': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
        'file_formatter': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'warning_formatter': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'style': '{',
        },
        'errors_formatter': {
            'format': '{asctime} {levelname} {message} {pathname}\n{exc_info}',
            'style': '{',
        },
    },
    'handlers': {
        'console_error': {
            'class': 'logging.StreamHandler',
            'formatter': 'errors_formatter',
            'filters': ['console_filter'],
            'level': 'ERROR',
        },
        'console_warning': {
            'class': 'logging.StreamHandler',
            'formatter': 'warning_formatter',
            'filters': ['console_filter'],
            'level': 'WARNING',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter',
            'filters': ['console_filter'],
            'level': 'DEBUG',
        },
        'general_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'general.log'),
            'formatter': 'file_formatter',
            'filters': ['file_email_filter'],
            'level': 'INFO',
        },
        'errors_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'errors.log'),
            'formatter': 'errors_formatter',
            'filters': ['file_email_filter'],
            'level': 'ERROR',
        },
        'email': {
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False,
            'formatter': 'warning_formatter',
            'level': 'ERROR',
            'filters': ['file_email_filter'],
        },
        'security_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'security.log'),
            'formatter': 'file_formatter',
            'filters': ['file_email_filter'],
        },
    },
    'loggers': {
        'django': {
            'handlers': [
                'console_error',
                'console_warning',
                'console',
                'general_file'
            ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['errors_file', 'email'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['errors_file', 'email'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file'],
            # 'level': 'DEBUG',
            'propagate': True,
        },
    },
    'root': {
        'handlers': [
            'console_error',
            'console_warning',
            'console',
            'general_file',
            'errors_file',
            'email',
            'security_file'
        ],
        'level': 'DEBUG',
    },
}