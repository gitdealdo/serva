from django.core.urlresolvers import reverse  # reverse_lazy
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse  # , HttpResponse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from backend_apps.utils.forms import empty
from ..models.tipo_menu import TipoMenu


class TipoMenuListView(LoginRequiredMixin, generic.ListView):
    """TipoMenuListView"""

    model = TipoMenu
    template_name = 'tipo_menu/list.html'
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
        context = super(TipoMenuListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Select %s to change') % capfirst(
            self.model._meta.verbose_name)
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context

    def post(self, request):

        nombre = request.POST.get('nombre', None)
        tipo_menu = request.POST.get('id_tipo_menu', None)

        if tipo_menu and nombre:
            """Actualizar tipo menu"""
            tm = TipoMenu.objects.get(id=tipo_menu)
            tm.nombre = nombre
            tm.save()
        elif nombre:
            """Crear tipo menu"""
            TipoMenu.objects.create(nombre=nombre)
        else:
            """Eliminar tipo menu"""
            TipoMenu.objects.get(id=request.POST['delete_id']).delete()

        # messages.success(request, msg)
        return HttpResponseRedirect(reverse("venta:tipo_menu_list"))


def crear_tipo_menu(request):
    if request.method == 'POST':
        tm = TipoMenu.objects.create(nombre=request.POST.get('nombre'))
        respuesta = {'id': tm.id, 'nombre': tm.nombre}
    return JsonResponse(respuesta)
