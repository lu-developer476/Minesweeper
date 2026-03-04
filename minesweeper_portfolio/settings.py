from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-B0WRmrbArbuvv5mxYIeM0jqjvp0G-fpPPuTwe9HuJtw")
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]

ALLOWED_HOSTS = _split_csv(os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1"))
CSRF_TRUSTED_ORIGINS = _split_csv(os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", ""))

# Render-safe defaults (avoid Bad Request 400 due to invalid Host header)
render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_hostname}")

if not DEBUG:
    # Works even when env vars are missing/misconfigured in Render dashboard.
    ALLOWED_HOSTS.append(".onrender.com")
    CSRF_TRUSTED_ORIGINS.append("https://*.onrender.com")

# De-duplicate while preserving order
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "game",
]

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

ROOT_URLCONF = "minesweeper_portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "minesweeper_portfolio.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Cordoba"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# Robust static serving on platforms where collectstatic artifacts may be unavailable
WHITENOISE_USE_FINDERS = True

# WhiteNoise storage. Manifest mode can crash with 500 if manifest is missing.
USE_MANIFEST_STATICFILES = os.getenv("DJANGO_USE_MANIFEST_STATICFILES", "0") == "1"
static_backend = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
    if USE_MANIFEST_STATICFILES
    else "whitenoise.storage.CompressedStaticFilesStorage"
)
STORAGES = {
    "staticfiles": {
        "BACKEND": static_backend,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Session backend: avoid DB dependency for gameplay state in cloud deploys.
# Can be overridden with DJANGO_SESSION_ENGINE if needed.
SESSION_ENGINE = os.getenv("DJANGO_SESSION_ENGINE", "django.contrib.sessions.backends.signed_cookies")

# Security (reasonable defaults for portfolio deploy)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = os.getenv("DJANGO_SESSION_COOKIE_SECURE", "0") == "1"
CSRF_COOKIE_SECURE = os.getenv("DJANGO_CSRF_COOKIE_SECURE", "0") == "1"
