from .base import *

INSTALLED_APPS += [
    "coverage",
    "debug_toolbar",
    "docutils",
    "django_extensions",
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

DEBUG = True

if DEBUG:

    def show_toolbar(request):
        if not request.is_ajax() and request.user:
            return True
        return False

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': 'config.settings.local.show_toolbar',
    }

STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}
