from django.conf.urls import url
from .views import tipo_menu
from .views import menu

urlpatterns = [

    url(r'^tipo_menu/lista/$', tipo_menu.TipoMenuListView.as_view(), name='tipo_menu_list'),
    url(r'^menu/lista/$', menu.MenuListView.as_view(), name='menu_list'),

    # url(r'^receta/editar/(?P<pk>[^/]+)/$', rec.RecetaUpdateView.as_view(), name='receta_edit'),
]
