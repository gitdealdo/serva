# import json
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
# from django.core import serializers
from django.utils.encoding import force_text
from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
from backend_apps.utils.security import log_params, get_dep_objects  # , SecurityKey, UserToken
# from decimal import Decimal
from ..models.unidad import Unidad
from ..forms.unidad import UnidadForm


class UnidadListView(generic.ListView):
    """UnidadListView"""

    model = Unidad
    template_name = 'unidad/list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UnidadListView, self).dispatch(request, *args, **kwargs)

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
        context = super(UnidadListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['form'] = UnidadForm
        context['title'] = _('Select %s to change') % capfirst(self.model._meta.verbose_name)
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context

    def post(self, request):
        print(request.POST)
        try:
            delete = request.POST['delete']
        except Exception:
            delete = None
        if delete:
            """Eliminar"""
            Unidad.objects.get(id=request.POST['delete']).delete()
            messages.success(request, 'Unidad eliminada con éxito')
        elif request.POST['id_unidad']:
            """Actualizar"""
            u = Unidad.objects.get(id=request.POST['id_unidad'])
            u.nombre = request.POST['nombre']
            u.simbolo = request.POST['simbolo']
            u.save()
            messages.success(request, 'Unidad %s actualizada con éxito' % u)
        else:
            """Crear"""
            u = Unidad(
                nombre=request.POST['nombre'],
                simbolo=request.POST['simbolo']
            )
            u.save()
            print("Creando")
            messages.success(request, 'Unidad %s registrada con éxito' % u)

        return HttpResponseRedirect(reverse('recetario:unidad_list'))


def crear_unidad(request):
    """crear unidad por ajax"""
    if request.method == 'POST':
        uni = Unidad.objects.create(
            nombre=request.POST.get('nombre'),
            simbolo=request.POST.get('simbolo'))
        respuesta = {'id': uni.id, 'nombre': uni.nombre}
    return JsonResponse(respuesta)
