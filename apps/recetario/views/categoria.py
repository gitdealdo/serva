from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
# from django.utils.encoding import force_text
from django.contrib.auth.mixins import LoginRequiredMixin
from backend_apps.utils.forms import empty

from ..models.categoria import Categoria
from ..forms.categoria import CategoriaForm


class CategoriaListView(LoginRequiredMixin, generic.ListView):
    """CategoriaListView"""

    model = Categoria
    template_name = 'categoria/list.html'
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
        context = super(CategoriaListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['form'] = CategoriaForm
        context['title'] = _('Select %s to change') % capfirst(
            self.model._meta.verbose_name)
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context

    def post(self, request):

        if request.POST['delete']:
            print("Eliminando")
            Categoria.objects.get(id=request.POST['delete']).delete()
            msg = ('Categoria eliminado con éxito')
        elif request.POST['id_tipo']:
            """Actualizar"""
            print("Actualizando")
            t = Categoria.objects.get(id=request.POST['id_tipo'])
            t.nombre = request.POST['nombre']
            t.save()
            msg = ('Categoria %s actualizado con éxito' % t)
        else:
            """Crear"""
            t = Categoria(
                nombre=request.POST['nombre']
            )
            t.save()
            msg = ('Categoria %s creado con éxito' % t)
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('recetario:categoria_list'))


def crear_categoria(request):
    """crear categoria producto por ajax"""
    if request.method == 'POST':
        categoria = Categoria.objects.create(nombre=request.POST.get('nombre'))
        respuesta = {'id': categoria.id, 'nombre': categoria.nombre}
    return JsonResponse(respuesta)
