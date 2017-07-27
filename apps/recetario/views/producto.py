import json
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
# from django.core import serializers
from django.utils.encoding import force_text
from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
from backend_apps.utils.security import log_params, get_dep_objects  # , SecurityKey, UserToken
# from decimal import Decimal
# from ..utils import defaultencode
from ..models.producto import Producto
from ..forms.producto import ProductoForm


class ProductoListView(generic.ListView):
    """ProductoListView"""

    model = Producto
    template_name = 'producto/list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'nombre')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(ProductoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Select %s to change') % capfirst(self.model._meta.verbose_name)
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class ProductoCreateView(generic.CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/form.html'
    success_url = reverse_lazy('recetario:producto_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoCreateView, self).dispatch(request, *args, **kwargs)

    # def get_success_url(self):
    #     return reverse('icontrol:detalle_producto_add', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ProductoCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Agregar %s') % ('Producto')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
        return super(ProductoCreateView, self).form_valid(form)


class ProductoUpdateView(generic.UpdateView):
    model = Producto
    template_name = 'producto/form.html'
    form_class = ProductoForm
    success_url = reverse_lazy('recetario:producto_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductoUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Actualizar %s') % ('Producto')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        msg = _('%(name)s "%(obj)s" fue cambiado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
        return super(ProductoUpdateView, self).form_valid(form)


class ProductoDeleteView(generic.DeleteView):
    model = Producto
    success_url = reverse_lazy('recetario:producto_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):

        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.success_url)
        return super(ProductoDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(self.request, ('No se puede Eliminar %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name)) + '\
                     "' + force_text(d) + '"'
                })
                raise Exception(msg)

            d.delete()
            msg = _(' %(name)s "%(obj)s" fue eliminado satisfactorialmente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# class ProductoCompleteTemplateView(generic.TemplateView):

#     def get(self, request, *args, **kwargs):

#         catego = request.GET.get('cat')
#         if catego:
#             productos = Producto.objects.filter(
#                 codigo__icontains=request.GET.get('query')).filter(categoria_id=catego)
#         else:
#             productos = Producto.objects.filter(
#                 codigo__icontains=request.GET.get('query'))

#         data = []

#         for p in productos:
#             producto_json = {}
#             prod = "%s" % (p.codigo)
#             producto_json['label'] = prod
#             producto_json['value'] = p.id
#             data.append(producto_json)

#         data_json = json.dumps(data)

#         return HttpResponse(data_json, content_type='application/json')




# class ProductoDetailView(generic.DetailView):
#     """ProductoDetailView"""
#     model = Producto
#     template_name = 'icontrol/producto/detalle.html'

#     def get_context_data(self, **kwargs):
#         context = super(ProductoDetailView, self).get_context_data(**kwargs)
#         context['opts'] = self.model._meta
#         context['title'] = _('Detalles del %s') % _('producto')
#         return context


# class ProductoFiltrarView(generic.ListView):
#     """docstring for ProductoFiltrarView"""

#     model = Producto
#     template_name = "icontrol/producto/productos.html"
#     context_object_name = "productos"
#     paginate_by = settings.PER_PAGE

#     @method_decorator(permission_resource_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(ProductoFiltrarView, self).dispatch(request, *args, **kwargs)

#     def get_paginate_by(self, queryset):
#         if 'all' in self.request.GET:
#             return None
#         return generic.ListView.get_paginate_by(self, queryset)

#     def get_context_data(self, **kwargs):
#         context = super(ProductoFiltrarView, self).get_context_data(**kwargs)
#         context['opts'] = self.model._meta
#         context['title'] = _('Select %s to see') % capfirst(_('product'))
#         context['categorias'] = Categoria.objects.all()
#         context['marcas'] = Marca.objects.all()
#         return context

#     def get_queryset(self):
#         queryset = self.model.objects.all()
#         try:
#             categoria = self.request.GET['categoria']
#             marca = self.request.GET['marca']
#             modelo = self.request.GET['modelo']
#             codigo = self.request.GET['codigo']
#             if categoria and marca and modelo and codigo:
#                 queryset = queryset.filter(
#                     categoria=categoria, marca=marca,
#                     modelo__contains=modelo, codigo__contains=codigo)
#             elif categoria and marca and modelo:
#                 queryset = queryset.filter(categoria=categoria, marca=marca,
#                                            modelo__contains=modelo)
#             elif categoria and marca:
#                 queryset = queryset.filter(categoria=categoria, marca=marca)
#             elif categoria:
#                 queryset = queryset.filter(categoria=categoria)
#         except Exception:
#             categoria = None
#             marca = None
#             modelo = None
#             codigo = None
#         return queryset
#         # return self.model.objects.filter(**{column_contains: self.q})
