from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.text import capfirst

from backend_apps.utils.forms import empty
from backend_apps.utils.security import get_dep_objects

from ..forms.post import PostForm

from ..models.post import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post/list.html"
    paginate_by = settings.PER_PAGE

    def dispatch(self, request, *args, **kwargs):
        return super(PostListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        u"""get_paginate_by."""
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        u"""get_queryset."""
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'title')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(
            **{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        u"""get_context_data."""
        context = super(PostListView,
                        self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = ('Seleccione %s para cambiar'
                            ) % capfirst('Post')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post/form.html"
    success_url = reverse_lazy('blog:post_list')

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'post'
        context['title'] = "Agregar Post"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        msg = ('El %(name)s "%(obj)s" fue agregado satisfactoriamente') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)

        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post/form.html"
    success_url = reverse_lazy('blog:post_list')

    def dispatch(self, request, *args, **kwargs):
        return super(PostUpdateView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'post'
        context['title'] = "Actualizar Post"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        msg = ('El %(name)s "%(obj)s" fue actualizado    satisfactoriamente') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)

        return super(PostUpdateView, self).form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

    def dispatch(self, request, *args, **kwargs):
        # key = self.kwargs['pk']
        # pk = SecurityKey.is_valid_key(request, key, 'doc_del')
        # if not pk:
        #     return HttpResponseRedirect(self.success_url)
        # self.kwargs['pk'] = pk
        # try:
        #     self.get_object()
        # except Exception as e:
        #     messages.error(self.request, e)
        #     log.warning(force_text(e), extra=log_params(self.request))
        #     return HttpResponseRedirect(self.success_url)
        return super(PostDeleteView,
                     self).dispatch(request, *args, **kwargs)

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
            msg = (' %(name)s "%(obj)s" fuel eliminado satisfactorialmente.') % {
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
