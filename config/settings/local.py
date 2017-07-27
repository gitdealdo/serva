from .base import *

INSTALLED_APPS += [
    "coverage",
    'debug_toolbar',
    "docutils",
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'auth': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'backend_auth',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

if DEBUG:

    def show_toolbar(request):
        if not request.is_ajax() and request.user:
            return True
        return False


    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': 'config.settings.local.show_toolbar',
    }

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
