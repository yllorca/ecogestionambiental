import os
from dotenv import load_dotenv
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Loading .env file automatically
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ.get('DEBUG')) == "1"

ALLOWED_HOSTS = [os.environ.get("ENV_ALLOWED_HOST")]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'widget_tweaks',
    'tinymce',

    # Local Apps
    'apps.home',
    'apps.cliente',
    'apps.reclamo',
    'apps.panel',
    'apps.informe',

    # # all auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
]

SITE_ID = os.environ.get("SITE_ID")

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

CRISPY_TEMPLATE_PACK = "bootstrap4"

DEFAULT = {
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': 'link image preview codesample contextmenu table code lists',
    'toolbar1': 'formatselect | bold italic underline | alignleft aligncenter alignright alignjustify '
                '| bullist numlist | outdent indent | table | link image | codesample | preview code',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'inline': False,
    'statusbar': True,
    'width': 'auto',
    'height': 360,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webecogestion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'webecogestion.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DB_USERNAME=os.environ.get("POSTGRES_USER")
DB_PASSWORD=os.environ.get("POSTGRES_PASSWORD")
DB_HOST=os.environ.get("POSTGRES_HOST")
DB_PORT=os.environ.get("POSTGRES_PORT")
DB_DATABASE=os.environ.get("POSTGRES_DB")

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2', #"django.db.backends.postgresql",
        "NAME": DB_DATABASE,
        "USER": DB_USERNAME,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


LOGIN_REDIRECT_URL = reverse_lazy('panel:login_success')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media_cdn")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
    # '/var/www/static/',
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        # example: override normal Boto credentials specifically for Anymail
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY"),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_KEY"),
        "region_name": os.environ.get("AWS_REGION"),
        # override other default options
        "config": {
            "connect_timeout": 30,
            "read_timeout": 30,
        }
    },
}

EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
DEFAULT_FROM_EMAIL = "noreplay@ecogestionambiental.cl"  # if you don't already have this in setting""
SERVER_EMAIL = "noreplay@ecogestionambiental.cl"  # ditto (default from-email for Django errors)
EMAIL_MAIN = "Ecogestion Ambiental Ltda <noresponder@ecogestionambiental.cl>"
EMAIL_USE_TLS = True

