from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "replace-me"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
        "django.contrib.sessions",

    "rest_framework",
    "notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # ✅ REQUIRED
    "django.middleware.common.CommonMiddleware",
]


ROOT_URLCONF = "notifications_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ]
        },
    },
]


WSGI_APPLICATION = "notifications_service.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# RabbitMQ settings
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.environ.get("RABBITMQ_QUEUE", "notifications_queue")

TRAEFIK_BASE_URL = "http://localhost:80"
# settings.py (ALL SERVICES)

SECRET_KEY = "django-insecure-=&96#t4&pcgu(48@obm3x@(0&!o2d^q*=_m7)++-^i9mh*s5c5"

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_NAME = "shared_session"
SESSION_COOKIE_DOMAIN = "127.0.0.1"
SESSION_COOKIE_PATH = "/"

SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
