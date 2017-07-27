from django.core.urlresolvers import reverse  # reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
# from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect  # , HttpResponse
from django.conf import settings
# from django.core import serializers
# from django.utils.encoding import force_text
from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
# from backend_apps.utils.security import log_params, get_dep_objects  # , SecurityKey, UserToken
# from decimal import Decimal
from apps.recetario.models.receta import Receta

from ..models.detalle import Detalle
from ..models.tipo_menu import TipoMenu


class DetalleTemplateView(generic.TemplateView):
    """DetalleTemplateView"""

    model = Detalle
    template_name = 'detalle/index.html'

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DetalleTemplateView, self).dispatch(request, *args, **kwargs)

    # def get_paginate_by(self, queryset):
    #     if 'all' in self.request.GET:
    #         return None
    #     return generic.ListView.get_paginate_by(self, queryset)

    # def get_queryset(self):
    #     self.o = empty(self.request, 'o', '-id')
    #     self.f = empty(self.request, 'f', 'nombre')
    #     self.q = empty(self.request, 'q', '')
    #     column_contains = u'%s__%s' % (self.f, 'contains')
    #     return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(DetalleTemplateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Crear un nuevo menu')
        context['recetas'] = Receta.objects.all()
        context['tipo_menus'] = TipoMenu.objects.all()
        # context['o'] = self.o
        # context['f'] = self.f
        # context['q'] = self.q.replace('/', '-')
        return context

    # def post(self, request):

    #     try:
    #         nombre = request.POST.get('nombre')
    #     except Exception as e:
    #         nombre = None
    #         raise e
    #     try:
    #         tipo_menu = request.POST.get('id_tipo_menu')
    #     except Exception as e:
    #         tipo_menu = None
    #         raise e
    #     if tipo_menu and nombre:
    #         """Actualizar tipo menu"""
    #         tm = TipoMenu.objects.get(id=tipo_menu)
    #         tm.nombre = nombre
    #         tm.save()
    #     elif nombre:
    #         """Crear tipo menu"""
    #         TipoMenu.objects.create(nombre=nombre)
    #     else:
    #         """Eliminar tipo menu"""
    #         TipoMenu.objects.get(id=request.POST['delete_id']).delete()

    #     # messages.success(request, msg)
    #     return HttpResponseRedirect(reverse("venta:tipo_menu_list"))
