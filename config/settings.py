import os
from datetime import timedelta

from dotenv import load_dotenv
from kombu import Queue

from pathlib import Path

load_dotenv(override=True)
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True if os.getenv("DEBUG") == "True" else False

ALLOWED_URLS = [
    "youtube.com",
]  # допустимые URL для ссылок модели lesson поле video

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "django_celery_beat",
    "users",
    "on_learning",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend"),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SPECTACULAR_SETTINGS = {
    "TITLE": "User Management API",
    "DESCRIPTION": "API для регистрации, получения и удаления пользователей.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "POSTGRES_USER": os.getenv("POSTGRES_USER"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("HOST"),
        "PORT": os.getenv("PORT"),
    }
}

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

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "users:login"
LOGOUT_REDIRECT_URL = "/"

COVERAGE_REPORT_HTML_OUTPUT_DIR = "htmlcov"
COVERAGE_USE_CACHE = True
COVERAGE_PATH_EXCLUDES = [
    "migrations",
]
COVERAGE_MODULE_EXCLUDES = []

CORS_ALLOWED_ORIGINS = [
    "https://read-only.example.com",
    "https://read-and-write.example.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://read-and-write.example.com",
]

STRIPE_API_KEY = os.getenv("API_KEY_STRIPE")
SUCCESS_URL_SESSION = '"http://127.0.0.1:8000/"'

CELERY_BROKER_URL = os.getenv("REDIS_LOCATION")
CELERY_RESULT_BACKEND = os.getenv("REDIS_LOCATION")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_ACKS_LATE = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 28 * 60
CELERY_TASK_IGNORE_RESULT = False

CELERY_QUEUES = (
    Queue("default", routing_key="task.#"),
    Queue("high_priority", routing_key="high.#"),
    Queue("low_priority", routing_key="low.#"),
)
CELERY_ROUTES = {
    "myapp.tasks.high_prio_task": {"queue": "high_priority"},
    "myapp.tasks.low_prio_task": {"queue": "low_priority"},
}

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_SEND_EVENTS = True
CELERY_EVENT_QUEUE_EXPIRES = 60
CELERY_PREFETCH_MULTIPLIER = 1
CELERY_MAX_MEMORY_PER_CHILD = 100000
CELERY_TASK_RETRY_ON_EXCEPTION = True
CELERY_TASK_MAX_RETRIES = 3
