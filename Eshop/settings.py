
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '-95t%=#4o3@l-(-%ok9*h%n3!0(sdchjn%+_$5#umaj-!3bg*7'
DEBUG = True
ALLOWED_HOSTS = []

CSRF_TRUSTED_ORIGINS = ['https://*.github.dev','https://*.127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp',
    'corsheaders',
    'store'
]

MIDDLEWARE = [
    'store.middlewares.csp.CSPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'https://maxcdn.bootstrapcdn.com',
    'https://code.jquery.com',
    'https://cdnjs.cloudflare.com',
    'https://use.fontawesome.com',
    'https://checkout.stripe.com',
)

ROOT_URLCONF = 'Eshop.urls'
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

WSGI_APPLICATION = 'Eshop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

AUTH_USER_MODEL = 'store.CustomUser'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = "/image/download/"
MEDIA_ROOT = BASE_DIR
STRIPE_PUBLIC_KEY = "pk_test_51NZ4ZdEiMppiGgYySDrgAESxJDbOa0PEHnmvxZ3kaU6274TtLAKjywiD8cNovZUZCLVmJJEcax8o5Fc7ms3cGjPJ00WS5XOzE8"
STRIPE_SECRET_KEY = "sk_test_51NZ4ZdEiMppiGgYyYU9PA9fe1b5GO0qqcwR4RZmWMBqRT4UoiPJm5JUpLX1loIRJJ4NT8obchxnOZDjdzNRfq8Rc00sRfZ6PSB"
