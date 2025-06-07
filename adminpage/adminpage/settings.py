"""
settings.py ― Django settings for adminpage project
Compatible with the revised docker-compose + Nginx volumes layout.
"""

import os
from datetime import timedelta

PREFIX = os.getenv("PREFIX", "")
# ────────────────────────────────────────────────────────────
# Utilities
# ────────────────────────────────────────────────────────────
def getenv_boolean(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    return value.upper() in ("TRUE", "1") if value is not None else default


def compose_base_url(schema: str, hostname: str, port) -> str:
    url = f"{schema}://{hostname}"
    if port and int(port) != 80:
        url += f":{port}"
    return url


# ────────────────────────────────────────────────────────────
# Sentry (optional)
# ────────────────────────────────────────────────────────────
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )


# ────────────────────────────────────────────────────────────
# Base / global constants
# ────────────────────────────────────────────────────────────
DATE_FORMAT = "%Y-%m-%d"

SELFSPORT_MINIMUM_MEDICAL_GROUP_ID = -1
SPORT_DEPARTMENT_EMAIL = "sport@innopolis.university"

STUDENT_AUTH_GROUP_VERBOSE_NAME = "Students"
STUDENT_AUTH_GROUP_NAME = "S-1-5-21-721043115-644155662-3522934251-2285"

TRAINER_AUTH_GROUP_VERBOSE_NAME = "School Physical Activity for Health"
TRAINER_AUTH_GROUP_NAME = "S-1-5-21-2948122937-1530199265-1034249961-9635"

SC_TRAINERS_GROUP_NAME_FREE = "SC trainers (free)"
SC_TRAINERS_GROUP_NAME_PAID = "SC trainers (paid)"
SELF_TRAINING_GROUP_NAME = "Self training"
EXTRA_EVENTS_GROUP_NAME = "Extra sport events"
MEDICAL_LEAVE_GROUP_NAME = "Medical leave"
OTHER_SPORT_NAME = "Other"

NOT_COPYABLE_GROUPS = [
    SELF_TRAINING_GROUP_NAME,
    EXTRA_EVENTS_GROUP_NAME,
    MEDICAL_LEAVE_GROUP_NAME,
]

TRAINING_EDITABLE_INTERVAL = timedelta(days=3)

BACHELOR_STUDY_PERIOD_YEARS = 4
BACHELOR_GROUPS_PREFIX = "B"
STUDENT_MAXIMUM_GROUP_COUNT = 5

SCHEMA = os.getenv("SCHEMA", "http")
HOSTNAME = os.getenv("HOSTNAME", "localhost")
PORT = os.getenv("PORT", 80)
BASE_URL = compose_base_url(SCHEMA, HOSTNAME, PORT)

PROJECT_ROOT = "/code/"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ────────────────────────────────────────────────────────────
# Security
# ────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = getenv_boolean("DEBUG")

ALLOWED_HOSTS = list(filter(None, os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")))
if DEBUG:
    ALLOWED_HOSTS.append("localhost")

if os.getenv("SCHEMA") == "https":
    # trust X-Forwarded-Proto set by the reverse proxy
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# ────────────────────────────────────────────────────────────
# Applications / middleware
# ────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.auth",
    "accounts",
    "revproxy",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_sendfile",
    "smartfields",
    "import_export",
    "rangefilter",
    "image_optimizer",
    "django_auth_adfs",
    "admin_auto_filters",
    "rest_framework",
    "django_prometheus",
    "sport.apps.SportConfig",
    "adminpage.apps.SportAdminConfig",
    "api",
    "media",
    "hijack",
    "hijack.contrib.admin",
    "tinymce",
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
    "hijack.middleware.HijackUserMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",  # enable if serving static without Nginx
]

ROOT_URLCONF = "adminpage.urls"
WSGI_APPLICATION = "adminpage.wsgi.application"
SITE_ID = 1


# ────────────────────────────────────────────────────────────
# Templates
# ────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_ROOT, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]


# ────────────────────────────────────────────────────────────
# Caches
# ────────────────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
    }
}


# ────────────────────────────────────────────────────────────
# Authentication / REST
# ────────────────────────────────────────────────────────────
AUTH_USER_MODEL = "accounts.User"

OAUTH_CLIENT_ID = os.getenv("oauth_appID", "?")
OAUTH_CLIENT_SECRET = os.getenv("oauth_shared_secret", "?")
OAUTH_AUTHORIZATION_BASEURL = os.getenv("oauth_authorization_baseURL", "?")
OAUTH_GET_INFO_URL = os.getenv("oauth_get_infoURL", "?")
OAUTH_TOKEN_URL = os.getenv("oauth_tokenURL", "?")
OAUTH_END_SESSION_URL = os.getenv("oauth_end_session_endpoint", "?")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "adminpage.authentication.InNoHassleAuthentication",
        "django_auth_adfs.rest_framework.AdfsAccessTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "InnoSport",
    "DESCRIPTION": """
### About this project

API for InnoSport platform (Innopolis University).
""",
    "VERSION": "v1",
    "CONTACT": {"name": "one-zero-eight", "url": "https://t.me/one_zero_eight"},
    "LICENSE": {"name": "MIT License", "identifier": "MIT"},
    "SERVERS": [
        {"url": "/api", "description": "Current"},
        {"url": "https://sport.innopolis.university/api", "description": "Production"},
        {"url": "https://stage.sport.innopolis.university/api", "description": "Staging"},
    ],
    "SCHEMA_PATH_PREFIX": "/api",
    "SCHEMA_PATH_PREFIX_TRIM": True,
    "OAS_VERSION": "3.1.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_SPLIT_PATCH": True,
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SWAGGER_UI_SETTINGS": {"tryItOutEnabled": True, "persistAuthorization": True, "filter": True},
    "AUTHENTICATION_WHITELIST": ["adminpage.authentication.InNoHassleAuthentication"],
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "django_auth_adfs.backend.AdfsAuthCodeBackend",
    "django_auth_adfs.backend.AdfsAccessTokenBackend",
)

AUTH_ADFS = {
    "SERVER": "sso.university.innopolis.ru",
    "CLIENT_ID": OAUTH_CLIENT_ID,
    "CLIENT_SECRET": OAUTH_CLIENT_SECRET,
    "RELYING_PARTY_ID": OAUTH_CLIENT_ID,
    "AUDIENCE": f"microsoft:identityserver:{OAUTH_CLIENT_ID}",
    "CA_BUNDLE": True,
    "USERNAME_CLAIM": "upn",
    "GROUPS_CLAIM": None,
    "CLAIM_MAPPING": {"first_name": "given_name", "last_name": "family_name", "role": "role"},
}

AUTH_INNOHASSLE = {
    "API_URL": "https://api.innohassle.ru/accounts/v0",
    "KEYS_RELOAD_INTERVAL": 24,
    "AUDIENCE": "sport",
    "USERNAME_CLAIM": "email",
}

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "profile"


# ────────────────────────────────────────────────────────────
# CORS
# ────────────────────────────────────────────────────────────
CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://innohassle\.ru$",
    r"^https://\w+\.innohassle\.ru$",
    r"^https://local\.innohassle\.ru:3000$",
]


# ────────────────────────────────────────────────────────────
# Database (PostgreSQL + Prometheus)
# ────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django_prometheus.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_SERVER"),
        "PORT": "",  # default 5432
    }
}
PROMETHEUS_EXPORT_MIGRATIONS = False


# ────────────────────────────────────────────────────────────
# Password validation
# ────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ────────────────────────────────────────────────────────────
# I18N / L10N
# ────────────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Moscow"
USE_I18N = USE_L10N = USE_TZ = True


# ────────────────────────────────────────────────────────────
# Static / media
# ────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = "/static"       # volume: django-static

MEDIA_URL = "/files/"
MEDIA_ROOT = "/media"         # volume: uploaded_media

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "adminpage.storage.CustomManifestStaticFilesStorage"},
}

# Sendfile via Nginx X-Accel
SENDFILE_BACKEND = "django_sendfile.backends.nginx"
SENDFILE_ROOT = MEDIA_ROOT
SENDFILE_URL = "/files/"


# ────────────────────────────────────────────────────────────
# File / image constraints
# ────────────────────────────────────────────────────────────
MEDICAL_REFERENCE_FOLDER = "medical_references"
SELF_SPORT_FOLDER = "self_sport_reports"
MEDICAL_GROUP_REFERENCE_FOLDER = "medical_group_references"

OPTIMIZED_IMAGE_METHOD = "pillow"
MAX_IMAGE_SIZE = 10_000_000  # 10 MB
MIN_IMAGE_DIMENSION = 400
MAX_IMAGE_DIMENSION = 4500


# ────────────────────────────────────────────────────────────
# Email
# ────────────────────────────────────────────────────────────
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ────────────────────────────────────────────────────────────
# Email templates (unchanged)
# ────────────────────────────────────────────────────────────
EMAIL_TEMPLATES = {
    # … (оставлены без изменений, см. исходный файл)
    # --- trimmed for brevity ---
}


# ────────────────────────────────────────────────────────────
# Academic duration rules
# ────────────────────────────────────────────────────────────
ACADEMIC_DURATION_PERCENTAGE = 0.05
ACADEMIC_DURATION_MAX = 2


# ────────────────────────────────────────────────────────────
# Logging
# ────────────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler"},
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "django.server",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "django.server": {"handlers": ["django.server"], "level": "INFO", "propagate": False},
    },
}


# ────────────────────────────────────────────────────────────
# Misc
# ────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"