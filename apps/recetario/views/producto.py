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
from ..models.tipo import Tipo
from ..models.unidad import Unidad
from ..forms.producto import ProductoForm, UploadFileForm
from pyexcel_xlsx import get_data


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
        context['form'] = UploadFileForm()
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


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            data = get_data(request.FILES['file'])
            insumos = list(data['Hoja1'])
            del insumos[0]
            for d in insumos:
                if not d:
                    break
                try:
                    categoria = Tipo.objects.get(nombre=d[9])
                except Exception:
                    categoria = Tipo.objects.create(nombre=d[9])
                try:
                    unidad = Unidad.objects.get(nombre=d[4])
                except Exception:
                    unidad = Unidad.objects.create(nombre=d[4])
                try:
                    producto = Producto.objects.get(nombre=d[2])
                except Exception:
                    producto = None

                if producto:
                    producto.descripcion = d[3]
                    producto.stock_minimo = d[5]
                    producto.stock = d[6]
                    producto.costo = d[7]
                    producto.save()
                else:
                    p = Producto()
                    p.nombre = d[2]
                    p.descripcion = d[3]
                    p.stock_minimo = d[5]
                    p.stock = d[6]
                    p.categoria = categoria
                    p.unidad = unidad
                    p.costo = d[7]
                    p.save()
            messages.success(request, "Insumos registrados y actualizados con éxito!")
            return HttpResponseRedirect(reverse('recetario:producto_list'))
