# billing_api/settings.py
from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY','secret-key')
DEBUG = os.getenv('DEBUG','True') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
  'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
  'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
  'rest_framework','django_filters',
  'users','catalog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required for sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for auth
    'django.contrib.messages.middleware.MessageMiddleware',  # Required for messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ADD THESE MISSING CONFIGURATIONS:
ROOT_URLCONF = 'billing_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'billing_api.wsgi.application'

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES':(
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ),
  'DEFAULT_PERMISSION_CLASSES':(
    'rest_framework.permissions.IsAuthenticated',
  ),
  'DEFAULT_FILTER_BACKENDS':(
    'django_filters.rest_framework.DjangoFilterBackend',
    'rest_framework.filters.SearchFilter',
    'rest_framework.filters.OrderingFilter',
  ),
  'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
  'PAGE_SIZE':10
}

DATABASES={
  'default':{
    'ENGINE':'django.db.backends.postgresql',
    'NAME':os.getenv('DB_NAME','programacioniv'),
    'USER':os.getenv('DB_USER','postgres'),
    'PASSWORD':os.getenv('DB_PASS','admin'),
    'HOST':os.getenv('DB_HOST','localhost'),
    'PORT':os.getenv('DB_PORT','5432')
  }
}

SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
  'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# ADD PASSWORD VALIDATORS AND INTERNATIONALIZATION
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL='static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'