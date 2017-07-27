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

from ..models.tipo import Tipo
from ..forms.tipo import TipoForm


class TipoListView(generic.ListView):
    """TipoListView"""

    model = Tipo
    template_name = 'tipo/list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TipoListView, self).dispatch(request, *args, **kwargs)

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
        context = super(TipoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['form'] = TipoForm
        context['title'] = _('Select %s to change') % capfirst(self.model._meta.verbose_name)
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context

    def post(self, request):

        if request.POST['delete']:
            print("Eliminando")
            Tipo.objects.get(id=request.POST['delete']).delete()
            msg = ('Tipo eliminado con éxito')
        elif request.POST['id_tipo']:
            """Actualizar"""
            print("Actualizando")
            t = Tipo.objects.get(id=request.POST['id_tipo'])
            t.nombre = request.POST['nombre']
            t.save()
            msg = ('Tipo %s actualizado con éxito' % t)
        else:
            """Crear"""
            t = Tipo(
                nombre=request.POST['nombre']
            )
            t.save()
            msg = ('Tipo %s creado con éxito' % t)
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('recetario:tipo_list'))