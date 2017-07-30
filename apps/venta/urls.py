from django.conf.urls import url
from .views import tipo_menu
from .views import menu
from .views import detalle

urlpatterns = [

    url(r'^tipomenu/lista/$', tipo_menu.TipoMenuListView.as_view(),
        name='tipo_menu_list'),
    url(r'^menu/lista/$', menu.MenuListView.as_view(), name='menu_list'),
    url(r'^detalle/index/$', detalle.DetalleTemplateView.as_view(),
        name='detalle_index'),

    # url(r'^receta/editar/(?P<pk>[^/]+)/$', rec.RecetaUpdateView.as_view(),
    # name = 'receta_edit'),
]
