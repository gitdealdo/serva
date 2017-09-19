from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse  # , HttpResponse
from django.conf import settings
from django.utils.encoding import force_text
from django.contrib.auth.mixins import LoginRequiredMixin
from backend_apps.utils.decorators import ResourcePermissionMixin
from backend_apps.utils.forms import empty
from backend_apps.utils.security import get_dep_objects  # log_params, SecurityKey, UserToken

from ..models.menu import Menu
from ..forms.menu import MenuForm
from ..models.tipo_menu import TipoMenu


class MenuListView(LoginRequiredMixin, generic.ListView):
    """MenuListView"""

    model = Menu
    template_name = 'menu/list.html'
    paginate_by = settings.PER_PAGE

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-fecha')
        self.f = empty(self.request, 'f', 'fecha')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(MenuListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Select %s to change') % capfirst(self.model._meta.verbose_name)
        context['tipos'] = TipoMenu.objects.all()
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class MenuCreateView(ResourcePermissionMixin, generic.CreateView):
    model = Menu
    form_class = MenuForm
    template_name = "menu/form.html"
    # success_url = reverse_lazy('venta:menu_list')

    def get_success_url(self):
        return reverse('venta:detalle_menu', kwargs={'menu': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user
        msg = ('El %(name)s "%(obj)s" fue agregado satisfactoriamente') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)
        return super(MenuCreateView, self).form_valid(form)


class MenuUpdateView(ResourcePermissionMixin, generic.UpdateView):
    model = Menu
    form_class = MenuForm
    template_name = "menu/form.html"
    success_url = reverse_lazy('venta:menu_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        msg = ('El %(name)s "%(obj)s" fue actualizado satisfactoriamente') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)
        return super(MenuUpdateView, self).form_valid(form)


class MenuDeleteView(ResourcePermissionMixin, generic.DeleteView):
    model = Menu
    success_url = reverse_lazy('venta:menu_list')

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
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

        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


def marcar_menu(request):
    print(request.GET)
    menu = Menu.objects.get(id=request.GET.get('menu'))
    menu.atendido = False if menu.atendido else True
    menu.save()
    btn_info = 'btn-success' if menu.atendido else 'btn-warning'
    btn_msg = 'Antendido' if menu.atendido else 'Marcar como atendido'
    return JsonResponse({'btn_info': btn_info, 'btn_msg': btn_msg})
