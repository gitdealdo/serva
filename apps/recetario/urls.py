from django.conf.urls import url
from .views import producto
from .views import receta as rec
from .views import categoria
from .views import unidad
from .views import tipo

urlpatterns = [

    # url(r'^dashboard/$', TemplateView.as_view(template_name="mod_backend/base
    # _mod_backend.html"), name='dashboard'),
    # url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^producto/listar/$', producto.ProductoListView.as_view(), name='producto_list'),
    url(r'^producto/crear/$', producto.ProductoCreateView.as_view(), name='producto_add'),
    url(r'^producto/(?P<pk>[^/]+)/editar/$', producto.ProductoUpdateView.as_view(),
        name='producto_edit'),
    url(r'^producto/(?P<pk>[^/]+)/eliminar/$', producto.ProductoDeleteView.as_view(),
        name='producto_delete'),
    url(r'^unidad/listar/$', unidad.UnidadListView.as_view(), name='unidad_list'),
    url(r'^tipo/listar/$', tipo.TipoListView.as_view(), name='tipo_list'),
    url(r'^categoria/listar/$', categoria.CategoriaListView.as_view(), name='categoria_list'),
    url(r'^receta/listar/$', rec.RecetaListView.as_view(), name='receta_list'),
    url(r'^receta/crear/$', rec.RecetaCreateView.as_view(), name='receta_add'),
    url(r'^receta/(?P<pk>[^/]+)/$', rec.RecetaDetailView.as_view(), name='receta_detail'),
    url(r'^receta/(?P<pk>[^/]+)/editar/$', rec.RecetaUpdateView.as_view(), name='receta_edit'),
    url(r'^receta/(?P<pk>[^/]+)/eliminar/$', rec.RecetaDeleteView.as_view(),
        name='receta_delete'),
]
