```python
"""
Django settings for ats_analyzer project.

Configured for Vercel deployment.
"""

from pathlib import Path
import os
import shutil


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-this-secret-key"
)

DEBUG = False

ALLOWED_HOSTS = [
    "*",
]

CSRF_TRUSTED_ORIGINS = [
    "https://ats-resume-analyzer-lilac.vercel.app",
    "https://*.vercel.app",
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "analyzer",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "ats_analyzer.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = "ats_analyzer.wsgi.application"


# ============================================================
# DATABASE
# ============================================================

# Vercel's deployed filesystem is read-only.
# /tmp is writable during a serverless execution.

SOURCE_DB = BASE_DIR / "db.sqlite3"

VERCEL_DB = Path("/tmp/db.sqlite3")


# Copy the existing SQLite database to the writable /tmp directory.
if SOURCE_DB.exists() and not VERCEL_DB.exists():
    try:
        shutil.copy2(SOURCE_DB, VERCEL_DB)
    except Exception:
        pass


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",

        "NAME": VERCEL_DB,

        "OPTIONS": {
            "timeout": 20,
        },
    }
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# WhiteNoise configuration
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# AUTHENTICATION
# ============================================================

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "/dashboard/"

LOGOUT_REDIRECT_URL = "/accounts/login/"


# ============================================================
# SESSION
# ============================================================

# Store sessions in signed cookies instead of the database.
# This avoids unnecessary database writes during login.

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


# ============================================================
# SECURITY FOR VERCEL
# ============================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = False


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```
