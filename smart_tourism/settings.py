"""
Smart Tourism Management System
Django Settings — Production-ready configuration
"""

import os
from datetime import timedelta
from pathlib import Path
from decouple import config

# ============================================================
# BASE
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='change-me-in-production')
DEBUG = config('DEBUG', default=False, cast=bool)
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
ALLOWED_HOSTS = ["travel-tourism-management-ifm3.onrender.com","smarttourism.vercel.app","localhost","127.0.0.1",]

# ============================================================
# APPLICATIONS
# ============================================================
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'django_celery_beat',
    'django_celery_results',
]

LOCAL_APPS = [
    'apps.users',
    'apps.places',
    'apps.bookings',
    'apps.cabs',
    'apps.reviews',
    'apps.travel_plans',
    'apps.payments',
    'apps.analytics',
    'apps.notifications',
    'ai_assistant',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ============================================================
# MIDDLEWARE
# ============================================================
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',           # Static files
#     'corsheaders.middleware.CorsMiddleware',                # CORS
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'apps.analytics.middleware.VisitorTrackingMiddleware',  # Custom tracking
# ]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'apps.analytics.middleware.VisitorTrackingMiddleware',
]
ROOT_URLCONF = 'smart_tourism.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'smart_tourism.wsgi.application'

# ============================================================
# DATABASE — MySQL
# ============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================================
# CUSTOM USER MODEL
# ============================================================
AUTH_USER_MODEL = 'users.User'

# ============================================================
# PASSWORD VALIDATION
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================
REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Permissions — default require login; override per-view
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'smart_tourism.pagination.StandardResultsPagination',
    'PAGE_SIZE': 10,
    # Filtering
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # Renderers
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    # Throttling
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    # Exception handler
    'EXCEPTION_HANDLER': 'smart_tourism.exceptions.custom_exception_handler',
}

# ============================================================
# JWT CONFIGURATION
# ============================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=config('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', default=60, cast=int)
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=config('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=7, cast=int)
    ),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# # ============================================================
# # CORS
# # ============================================================
# CORS_ALLOWED_ORIGINS = [
#     config('FRONTEND_URL', default='http://localhost:3000'),
#     'http://localhost:5173',
#     'http://localhost:5174',
#     'http://127.0.0.1:5173',
#     'http://127.0.0.1:5174',
# ]
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = [
#     'accept', 'accept-encoding', 'authorization', 'content-type',
#     'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
# ]
# ============================================================
# CORS
# ============================================================

CORS_ALLOWED_ORIGINS = [
    "https://smarttourism.vercel.app",

    # Local Development
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CSRF_TRUSTED_ORIGINS = [
    "https://smarttourism.vercel.app",
]

# ============================================================
# STATIC & MEDIA
# ============================================================
STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# CACHING
# ============================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'smart-tourism-local-cache',
        'TIMEOUT': 300,
    }
}

# ============================================================
# CELERY
# ============================================================
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
from smart_tourism.beat_schedule import CELERY_BEAT_SCHEDULE  # noqa: E402
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

# ============================================================
# EMAIL
# ============================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER', default='noreply@smarttourism.com')

# ============================================================
# EXTERNAL APIS
# ============================================================
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='')
GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID', default='')
WEATHER_API_KEY = config('WEATHER_API_KEY', default='')
WEATHER_API_URL = config('WEATHER_API_URL', default='https://api.openweathermap.org/data/2.5/weather')

# ============================================================
# LOGGING
# ============================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ============================================================
# INTERNATIONALISATION
# ============================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# SWAGGER / API DOCS
# ============================================================
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

# ============================================================
# FILE UPLOAD LIMITS
# ============================================================
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024    # 10 MB
