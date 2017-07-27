
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf.global_settings import STATICFILES_DIRS, MEDIA_ROOT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4i$*sc0-_ih(xvd)mbjlfl7y3d1e1j01vizd)d07llb5f6eg(v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # added
    'django.contrib.sites',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'crispy_forms',

    # mis tools
    'backend_apps.utils',
    'debug_toolbar',
    # mis apps
    'backend_apps.auths',
    'backend_apps.access',

    'apps.blog.apps.BlogConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # added
    'django.middleware.locale.LocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

ROOT_URLCONF = 'config.urls'

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

                'django.template.context_processors.i18n',
                # 'django.core.context_processors.l10n',
                'django.template.context_processors.media',

                'django.template.context_processors.static',
                'django.template.context_processors.tz',

                # My context Processors
                'backend_apps.utils.context_processors.debug'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'auths.User'  # Custom User

SITE_ID = 1

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static_deploy")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# DESC
DESC = 'DESC'
if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    DESC = 'ASC'

from django.utils.translation import ugettext_lazy as _



CRISPY_TEMPLATE_PACK = 'bootstrap3'

PER_PAGE = 6


# Backup/restore database https://code.djangoproject.com/wiki/Fixtures
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)
LOGIN_URL = '/access/login/'

def show_toolbar(request):
    if not request.is_ajax() and request.user:
        return True
    return False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'config.settings.show_toolbar'
}