"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
# from backend_apps.access.views import home
from apps.recetario.views.receta import RecetaListView

# from django.views.i18n import javascript_catalog  # Deprecado desde la
# version 1.10 y eliminado 2.0

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # http://stackoverflow.com/questions/19625102/django-javascript-translation-not-working
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript_catalog'),
    url(r'^backend/', include('backend_apps.auths.urls', namespace='backend')),
    url(r'^access/', include('backend_apps.access.urls', namespace='access')),
    # url(r'^$', home, name='home'),

    url(r'^blog/', include('apps.blog.urls', namespace='blog')),
    url(r'^recetario/', include('apps.recetario.urls', namespace='recetario')),
    url(r'^venta/', include('apps.venta.urls', namespace='venta')),
    url(r'^$', RecetaListView.as_view(), name='home')


]
urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
