"""
Django settings for ofcors project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import multiprocessing
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from typing import Any
from uuid import uuid4

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("PROD", "0") == "0"

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = os.getenv("SECRET_KEY", "e6bc26ad-5398-4388-bd0e-9c71cc6b80d0")
else:
    SECRET_KEY = os.getenv("SECRET_KEY", str(uuid4()))

ALLOWED_HOSTS: list[str] = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "web",
    "corsheaders",
    "django_tables2",
    "django_filters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ofcors.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "ofcors.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

MAX_CONN_AGE = 600
DATABASES: dict[str, Any]

if "DATABASE_URL" in os.environ:
    # https://github.com/heroku/python-getting-started/blob/main/gettingstarted/settings.py

    DATABASES = {
        "default": dj_database_url.config(conn_max_age=MAX_CONN_AGE, ssl_require=True)
    }

    # Enable test database if found in CI environment.
    if "CI" in os.environ:
        DATABASES["default"]["TEST"] = DATABASES["default"]
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "web/staticfiles"  # destination of collectstatic
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_ALLOW_ALL_ORIGINS = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "log_to_stdout": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "web": {
            "handlers": ["log_to_stdout"],
            "level": "INFO" if not DEBUG else "DEBUG",
            "propagate": True,
        }
    },
}

# Target enumeration

HTTPS_TESTING_POOL_SIZE = int(
    os.getenv("HTTPS_TESTING_POOL_SIZE", multiprocessing.cpu_count())
)
HTTPS_TESTING_TIMEOUT = int(os.getenv("HTTPS_TESTING_TIMEOUT", 1.25))

# JS Payload

JS_REDIRECT_MS = int(os.getenv("JS_REDIRECT_MS", 1_000))

# CORS Configuration
# https://github.com/adamchainz/django-cors-headers#configuration

CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "1") == "1"

# Authentication

AUTH_TICKET_VALID_WINDOW_S = int(
    os.getenv("AUTH_TICKET_VALID_WINDOW_S", 60 * 5)
)  # 5 minutes

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Amass Integration

AMASS_LINUX_I386_DIR = "linux_i386"
AMASS_LINUX_I386_BIN = "amass"
AMASS_MACOS_AMD64_DIR = "macos_amd64"
AMASS_MACOS_AMD64_BIN = "amass"
AMASS_WINDOWS_AMD64_DIR = "windows_amd"
AMASS_WINDOWS_AMD64_BIN = "amass.exe"

_path_segments = []
if sys.platform == "linux" or sys.platform == "linux2":
    _path_segments = [AMASS_LINUX_I386_DIR, AMASS_LINUX_I386_BIN]
elif sys.platform == "darwin":
    _path_segments = [AMASS_MACOS_AMD64_DIR, AMASS_MACOS_AMD64_BIN]
else:
    # Assuming Windows here (this is incorrect but good enough for now)
    _path_segments = [AMASS_WINDOWS_AMD64_DIR, AMASS_WINDOWS_AMD64_BIN]
AMASS_BIN_PATH = os.path.join(BASE_DIR, "vendor", "amass", *_path_segments)

# Files

FILES_DIR = os.getenv("FILES_DIR", "files")
EXAMPLE_YML_FILE = os.getenv("EXAMPLE_YML_FILE", "example.yml")
EXAMPLE_YML_FILE_PATH = os.path.join(BASE_DIR, FILES_DIR, EXAMPLE_YML_FILE)
