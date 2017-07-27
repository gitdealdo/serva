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
    url(r'^producto/lista/$', producto.ProductoListView.as_view(), name='producto_list'),
    url(r'^producto/crear/$', producto.ProductoCreateView.as_view(), name='producto_add'),
    url(r'^producto/editar/(?P<pk>[^/]+)/$', producto.ProductoUpdateView.as_view(),
        name='producto_edit'),
    url(r'^producto/eliminar/(?P<pk>[^/]+)/$', producto.ProductoDeleteView.as_view(),
        name='producto_delete'),
    url(r'^unidad/lista/$', unidad.UnidadListView.as_view(), name='unidad_list'),
    url(r'^tipo/lista/$', tipo.TipoListView.as_view(), name='tipo_list'),
    url(r'^categoria/lista/$', categoria.CategoriaListView.as_view(), name='categoria_list'),
    url(r'^receta/lista/$', rec.RecetaListView.as_view(), name='receta_list'),
    url(r'^receta/crear/$', rec.RecetaCreateView.as_view(), name='receta_add'),
    url(r'^receta/detalle/(?P<pk>[^/]+)/$', rec.RecetaDetailView.as_view(), name='receta_detail'),
    url(r'^receta/editar/(?P<pk>[^/]+)/$', rec.RecetaUpdateView.as_view(), name='receta_edit'),
    url(r'^receta/eliminar/(?P<pk>[^/]+)/$', rec.RecetaDeleteView.as_view(),
        name='receta_delete'),
]