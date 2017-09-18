from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
from django.contrib import messages
from django.views import generic
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
# from django.conf import settings
# from django.core import serializers
from django.utils.encoding import force_text
# from backend_apps.utils.decorators import permission_resource_required
# from backend_apps.utils.forms import empty
from backend_apps.utils.security import log_params, get_dep_objects  # , SecurityKey, UserToken
from apps.recetario.models.receta import Receta
from apps.recetario.models.ingrediente import Ingrediente
from apps.recetario.models.producto import Producto

from ..models.detalle import Detalle
from ..models.insumos_detalle import InsumosDetalle
# from ..models.tipo_menu import TipoMenu
from ..models.menu import Menu
import json
import decimal

class DetalleTemplateView(generic.TemplateView):
    """DetalleTemplateView"""
    model = Detalle
    template_name = 'detalle/index.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleTemplateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['menu'] = Menu.objects.get(id=self.kwargs['menu'])
        context['detalles'] = Detalle.objects.filter(menu=self.kwargs['menu'])
        context['recetas'] = Receta.objects.all()
        context['insumos'] = Producto.objects.all()
        return context


class IngredienteListView(generic.ListView):
    model = Ingrediente
    template_name = "detalle/ingredientes.html"

    def get_queryset(self):
        qs = super(IngredienteListView, self).get_queryset()
        receta = Receta.objects.get(id=self.request.GET.get('receta'))
        porcion = self.request.GET.get('porcion')
        qs = qs.filter(receta=receta)
        for d in qs:
            cant_por_unidad = d.cantidad / receta.porcion
            d.cantidad_total = round((cant_por_unidad * int(porcion)), 2)
            if d.producto.stock >= d.cantidad_total:
                d.msg = "suficiente"
            else:
                diferencia = d.cantidad_total - d.producto.stock
                d.msg = "insuficiente| diferencia %s" % (round(diferencia, 2))
        return qs


def crear_detalle(request):
    if request.method == 'POST':
        menu = Menu.objects.get(id=request.POST['menu'])
        receta = Receta.objects.get(id=request.POST['receta'])
        detalle = Detalle()
        detalle.receta = receta
        detalle.porcion = int(request.POST['porcion'])
        detalle.menu = menu
        insumos = json.loads(request.POST['insumos'])
        print(insumos)
        costo = 0

        for d in insumos:
            cant = float(d['cantidad'])
            producto = Producto.objects.get(id=d['producto'])
            resto = producto.stock - cant
            cantidad = cant if cant < producto.stock else producto.stock
            # Actualizado producto
            producto.stock = resto if resto > 0 else 0
            producto.save()
            costo += producto.costo * decimal.Decimal(cantidad)
            insumodet = InsumosDetalle()
            insumodet.detalle = detalle
            insumodet.insumo = producto
            insumodet.cantidad = cantidad
            insumodet.save()
        detalle.costo = costo
        detalle.save()
    return JsonResponse({'receta': receta.nombre, 'porcion': request.POST['porcion']})


class DetalleListView(generic.ListView):
    model = Detalle
    template_name = "detalle/list.html"

    def get_context_data(self, **kwargs):
        context = super(DetalleListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['menu'] = Menu.objects.get(id=self.kwargs['menu'])
        context['btn_info'] = 'btn-success' if context['menu'].atendido else 'btn-warning'
        context['btn_msg'] = 'Antendido' if context['menu'].atendido else 'Marcar como atendido'
        return context

    def get_queryset(self):
        return self.model.objects.filter(menu=self.kwargs['menu'])


class DetalleDeleteView(generic.DeleteView):
    model = Detalle
    success_url = reverse_lazy('venta:detalle_list')

    def delete(self, request, *args, **kwargs):
        d = self.get_object()
        try:
            # d.insumosdetalle_set.all().delete()  # Eliminando dependencia
            for x in d.insumosdetalle_set.all():
                # Actualizado stock insumos
                x.insumo.stock += x.cantidad
                x.insumo.save()
                x.delete()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(
                    self.request,
                    ('No se puede eliminar %(name)s') %
                    {
                        "name": capfirst(force_text(
                            self.model._meta.verbose_name)
                        ) + '"' + force_text(d) + '"'
                    })
                raise Exception(msg)
            d.delete()
            msg = (' %(name)s "%(obj)s" fue eliminado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)

        except Exception as e:
            messages.error(request, e)

        self.success_url = reverse_lazy('venta:detalle_list', kwargs={'menu': d.menu.pk})
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
