import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-asknehru-replacement-backend-key",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "api.asknehru.com,localhost,127.0.0.1",
).split(",")
APPEND_SLASH = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "core.apps.CoreConfig",
    "auth",
    "users",
    "medicines",
    "conversations",
    "roadmaps",
    "yoga",
    "uploads",
    "planning",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "asknehru_django.urls"

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

WSGI_APPLICATION = "asknehru_django.wsgi.application"
ASGI_APPLICATION = "asknehru_django.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "demoappdb"),
        "USER": os.environ.get("POSTGRES_USER", "demoappuser"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "demoapp123"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.authentication.AskNehruJWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

ASKNEHRU_JWT_SECRET = os.environ.get(
    "ASKNEHRU_JWT_SECRET",
    "change-me-to-a-very-long-secret-at-least-32-characters",
)
ASKNEHRU_JWT_EXPIRATION_MS = int(os.environ.get("ASKNEHRU_JWT_EXPIRATION_MS", "3600000"))
ASKNEHRU_BASE_URL = os.environ.get("ASKNEHRU_BASE_URL", "https://api.asknehru.com")

ASKNEHRU_SHARED_UPLOAD_DIR = Path(
    os.environ.get("ASKNEHRU_SHARED_UPLOAD_DIR", str(BASE_DIR / "media" / "audio"))
)
ASKNEHRU_YOGA_IMAGE_UPLOAD_DIR = Path(
    os.environ.get("ASKNEHRU_YOGA_IMAGE_UPLOAD_DIR", str(BASE_DIR / "media" / "yoga-poses"))
)
ASKNEHRU_YOGA_AUDIO_UPLOAD_DIR = Path(
    os.environ.get("ASKNEHRU_YOGA_AUDIO_UPLOAD_DIR", str(BASE_DIR / "media" / "yoga-audio"))
)
ASKNEHRU_YOGA_VIDEO_UPLOAD_DIR = Path(
    os.environ.get("ASKNEHRU_YOGA_VIDEO_UPLOAD_DIR", str(BASE_DIR / "media" / "yoga-video"))
)