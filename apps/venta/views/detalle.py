from django.core.urlresolvers import reverse  # reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
# from django.contrib import messages
from django.views import generic
from django.http import JsonResponse  # HttpResponseRedirect , HttpResponse
# from django.conf import settings
# from django.core import serializers
# from django.utils.encoding import force_text
# from backend_apps.utils.decorators import permission_resource_required
# from backend_apps.utils.forms import empty
# from backend_apps.utils.security import log_params, get_dep_objects  # , SecurityKey, UserToken
# from decimal import Decimal
from apps.recetario.models.receta import Receta
from apps.recetario.models.ingrediente import Ingrediente
from apps.recetario.models.producto import Producto

from ..models.detalle import Detalle
from ..models.insumos_detalle import InsumosDetalle
from ..models.tipo_menu import TipoMenu
from ..models.menu import Menu
import json


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
                d.stock = "suficiente"
            else:
                d.stock = "insuficiente"
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
        costo = 0
        for d in insumos:
            producto = Producto.objects.get(id=d['producto'])
            costo += producto.costo * int(request.POST['porcion'])
            insumodet = InsumosDetalle()
            insumodet.detalle = detalle
            insumodet.insumo = producto
            insumodet.cantidad = d['cantidad']
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
        # context['insumos'] = Producto.objects.all()
        return context

    def get_queryset(self):
        return self.model.objects.filter(menu=self.kwargs['menu'])
