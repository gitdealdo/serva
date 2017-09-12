from django.conf.urls import url
from .views import producto
from .views import receta as rec
from .views import tipo_receta
from .views import unidad
from .views import categoria

urlpatterns = [

    # url(r'^dashboard/$', TemplateView.as_view(template_name="mod_backend/base
    # _mod_backend.html"), name='dashboard'),
    # url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^producto/lista/$',
        producto.ProductoListView.as_view(), name='producto_list'),
    url(r'^producto/crear/$',
        producto.ProductoCreateView.as_view(), name='producto_add'),
    url(r'^producto/(?P<pk>[^/]+)/editar/$',
        producto.ProductoUpdateView.as_view(),
        name='producto_edit'),
    url(r'^producto/(?P<pk>[^/]+)/eliminar/$',
        producto.ProductoDeleteView.as_view(),
        name='producto_delete'),
    url(r'^producto/upload/$',
        producto.upload_file, name='upload_file'),
    url(r'^unidad/lista/$',
        unidad.UnidadListView.as_view(), name='unidad_list'),
    url(r'^unidad/ajaxcrear/$', unidad.crear_unidad, name='unidad_crear'),
    url(r'^categoria/lista/$', categoria.CategoriaListView.as_view(), name='tipo_list'),
    url(r'^categoria/ajaxcrear/$',
        categoria.crear_categoria, name='crear_categoria'),
    url(r'^tiporeceta/lista/$', tipo_receta.TipoRecetaListView.as_view(),
        name='tipo_receta_list'),
    url(r'^tiporeceta/ajaxcrear/$', tipo_receta.crear_tipo_receta,
        name='tipo_receta_crear'),
    url(r'^receta/lista/$', rec.RecetaListView.as_view(), name='receta_list'),
    url(r'^receta/crear/$', rec.RecetaCreateView.as_view(), name='receta_add'),
    url(r'^receta/(?P<pk>[^/]+)/$',
        rec.RecetaDetailView.as_view(), name='receta_detail'),
    url(r'^receta/(?P<pk>[^/]+)/editar/$',
        rec.RecetaUpdateView.as_view(), name='receta_edit'),
    url(r'^receta/(?P<pk>[^/]+)/eliminar/$', rec.RecetaDeleteView.as_view(),
        name='receta_delete'),
]
