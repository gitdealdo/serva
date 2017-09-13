from django.conf.urls import url
from .views import tipo_menu
from .views import menu
from .views import detalle
from .views import insumos_detalle as det

urlpatterns = [

    url(r'^tipomenu/lista/$', tipo_menu.TipoMenuListView.as_view(),
        name='tipo_menu_list'),
    url(r'^tipomenu/ajaxcrear/$', tipo_menu.crear_tipo_menu,
        name='crear_tipo_menu'),
    url(r'^menu/lista/$', menu.MenuListView.as_view(), name='menu_list'),
    url(r'^menu/crear/$', menu.MenuCreateView.as_view(), name='menu_create'),
    url(r'^menu/(?P<pk>[^/]+)/editar/$', menu.MenuUpdateView.as_view(), name='menu_edit'),
    url(r'^menu/(?P<pk>[^/]+)/eliminar/$', menu.MenuDeleteView.as_view(), name='menu_delete'),
    url(r'^detalle/(?P<menu>[^/]+)/configurar/$', detalle.DetalleTemplateView.as_view(),
        name='detalle_menu'),
    url(r'^detalle/ingredientes/$', detalle.IngredienteListView.as_view(),
        name='filtrar_ingredientes'),
    url(r'^detalle/creardetalle/$', detalle.crear_detalle,
        name='crear_detalle'),
    url(r'^detalle/(?P<menu>[^/]+)/lista/$', detalle.DetalleListView.as_view(),
        name='detalle_list'),
    url(r'^detalle/(?P<pk>[^/]+)/eliminar/$', detalle.DetalleDeleteView.as_view(),
        name='detalle_delete'),
    url(r'^insumosdetalle/(?P<detalle>[^/]+)/crear/$', det.InsumosDetalleCreateView.as_view(),
        name='insumosdetalle_crear'),
    url(r'^insumosdetalle/(?P<pk>[^/]+)/eliminar/$', det.InsumosDetalleDeleteView.as_view(),
        name='insumosdetalle_delete'),
]
