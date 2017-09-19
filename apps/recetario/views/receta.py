# import json
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse  # , HttpResponse
from django.conf import settings
# from django.core import serializers
from django.utils.encoding import force_text
from backend_apps.utils.decorators import LoginRequiredMixin, ResourcePermissionMixin
from backend_apps.utils.forms import empty
# , SecurityKey, UserToken, log_params,
from backend_apps.utils.security import get_dep_objects
from ..models.receta import Receta
from ..forms.receta import RecetaForm
from ..models.producto import Producto
from ..models.ingrediente import Ingrediente


class RecetaListView(generic.ListView):
    """RecetaListView"""

    model = Receta
    template_name = 'receta/index.html'
    paginate_by = settings.PER_PAGE

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        qs = self.model.objects.filter(publicar=True)
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'nombre')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return qs.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(RecetaListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Select %s to change') % capfirst(
            self.model._meta.verbose_name)
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class RecetaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'receta/form.html'

    def get_success_url(self):
        return reverse('recetario:receta_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(RecetaCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Agregar %s') % (self.model._meta.verbose_name)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.autor = self.request.user
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
        return super(RecetaCreateView, self).form_valid(form)


class RecetaDetailView(generic.DetailView):
    """RecetaDetailView"""
    model = Receta
    template_name = 'receta/detail.html'

    def get_context_data(self, **kwargs):
        context = super(RecetaDetailView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Detalle %s') % (self.model._meta.verbose_name)
        context['productos'] = Producto.objects.all()
        context['label_info'] = 'label-success' if self.object.publicar else 'label-warning'
        context['label_msg'] = 'Publicado' if self.object.publicar else 'Aún no publicado'
        return context

    def post(self, request, *args, **kwargs):
        try:
            producto = request.POST.get('producto')
        except Exception as e:
            producto = None
            raise e
        if producto:
            ing = Ingrediente(
                producto=Producto.objects.get(id=request.POST['producto']),
                cantidad=request.POST['cantidad'],
                receta=Receta.objects.get(id=self.kwargs['pk'])
            )
            ing.save()
        else:
            Ingrediente.objects.get(id=request.POST['ingrediente_id']).delete()

        # return HttpResponseRedirect("") # OK
        # return redirect(RecetaDetailView.get(request))
        return HttpResponseRedirect(request.path)


class RecetaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Receta
    template_name = 'receta/form.html'
    form_class = RecetaForm

    def get_context_data(self, **kwargs):
        context = super(RecetaUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Actualizar %s') % (self.model._meta.verbose_name)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.success_url = reverse_lazy('recetario:receta_detail',
                                        kwargs={'pk': self.kwargs['pk']})

        msg = _('%(name)s "%(obj)s" fue actualizado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
        return super(RecetaUpdateView, self).form_valid(form)


class RecetaDeleteView(ResourcePermissionMixin, generic.DeleteView):
    model = Receta
    success_url = reverse_lazy('recetario:mis_recetas')

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            d.ingrediente_set.all().delete()
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


class MiRecetaListView(LoginRequiredMixin, generic.ListView):
    model = Receta
    template_name = "receta/list.html"

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        qs = self.model.objects.filter(autor=self.request.user)
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'nombre')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return qs.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(MiRecetaListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = _('Select %s to change') % capfirst(
            self.model._meta.verbose_name)
        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context
