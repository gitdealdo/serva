from django.core.urlresolvers import reverse  # reverse_lazy
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse  # , HttpResponse
from django.conf import settings
# from django.core import serializers
# from django.utils.encoding import force_text
from backend_apps.utils.decorators import LoginRequiredMixin
from backend_apps.utils.forms import empty
# from backend_apps.utils.security import log_params, get_dep_objects  # , SecurityKey, UserToken
# from decimal import Decimal

from ..models.tipo_receta import TipoReceta


class TipoRecetaListView(LoginRequiredMixin, generic.ListView):
    """TipoRecetaListView"""

    model = TipoReceta
    template_name = 'tipo_receta/list.html'
    paginate_by = settings.PER_PAGE

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
        context = super(TipoRecetaListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Select %s to change') % capfirst(
            self.model._meta.verbose_name)
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context

    def post(self, request):

        if request.POST['delete']:
            print("Eliminando")
            TipoReceta.objects.get(id=request.POST['delete']).delete()
            msg = ('TipoReceta eliminado con éxito')
        elif request.POST['id_categoria']:
            """Actualizar"""
            print("Actualizando")
            t = TipoReceta.objects.get(id=request.POST['id_categoria'])
            t.nombre = request.POST['nombre']
            t.save()
            msg = ('TipoReceta %s actualizado con éxito' % t)
        else:
            """Crear"""
            t = TipoReceta(
                nombre=request.POST['nombre']
            )
            t.save()
            msg = ('TipoReceta %s creado con éxito' % t)
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('recetario:tipo_receta_list'))


def crear_tipo_receta(request):
    if request.method == 'POST':
        cat = TipoReceta.objects.create(nombre=request.POST.get('nombre'))
        respuesta = {'id': cat.id, 'nombre': cat.nombre}
    return JsonResponse(respuesta)
