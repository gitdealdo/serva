from django.core.urlresolvers import reverse_lazy, reverse
from django.core import serializers
from django.contrib.auth.models import Group
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.text import capfirst
from django.utils.encoding import force_text

from backend_apps.utils.security import get_dep_objects


from ..models import User, Person
from ..forms.user import UserForm, UserPersonForm, PasswordChangeCustomForm
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)


class UserListView(generic.ListView):
    model = User
    template_name = "auths/user/list.html"

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = ('Seleccione %s para cambiar') % capfirst('usuario')
        return context


class UserPersonCreateView(generic.CreateView):
    u"""Crea usuario."""

    model = User
    template_name = "auths/user/form.html"
    form_class = UserForm
    success_url = reverse_lazy("backend:user_list")

    def get_context_data(self, **kwargs):
        context = super(UserPersonCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = ('Agregar %s') % capfirst('usuario')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        print(form.cleaned_data["email"])
        person = Person(
            identity_type=form.cleaned_data['identity_type'],
            identity_num=form.cleaned_data['identity_num'],
            cellphone=form.cleaned_data['cellphone'],
            birth_date=form.cleaned_data['birth_date'],
            address=form.cleaned_data['address'],
        )
        person.save()
        self.object.person = person
        # user = authenticate(username=self.request.POST[
        # 'username'], password=self.request.POST['password1'])

        # user_c = User.objects.get(username=self.object.username)
        # grupo = Group.objects.get(id=form.cleaned_data['grupo'])
        form.cleaned_data['grupo'].user_set.add(self.object)
        # grupo.user_set.add(user_c)
        # if user is not None:
        #     login(self.request, user)
        # this is the only time the user would be logged in.
        msg = ('El %(name)s "%(obj)s" fue creado satisfactoriamente') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)

        return super(UserPersonCreateView, self).form_valid(form)


class UserDeleteView(generic.DeleteView):
    model = User
    success_url = reverse_lazy('backend:user_list')

    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView,
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


class UserTemplateView(generic.TemplateView):

    model = User
    template_name = "auths/user/detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserTemplateView, self).get_context_data(**kwargs)
        print(serializers.serialize('json', [self.request.user.person, ]))
        context['opts'] = self.model._meta
        context['title'] = ('My %s') % capfirst('profile')
        return context


class UserPersonUpdateView(generic.UpdateView):
    u"""Actualizar usuario."""

    model = User
    template_name = "auths/user/userpersonform.html"
    form_class = UserPersonForm
    success_url = reverse_lazy("backend:user_profile")

    def get_initial(self):
        initial = super(UserPersonUpdateView, self).get_initial()
        initial = initial.copy()
        d = self.object
        initial['identity_type'] = d.person.identity_type
        initial['identity_num'] = d.person.identity_num
        initial['birth_date'] = d.person.birth_date
        initial['photo'] = d.person.photo
        initial['cellphone'] = d.person.cellphone
        initial['address'] = d.person.address
        initial['about'] = d.person.about
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=True)
        print(form.cleaned_data["email"])
        p = self.object.person
        p.identity_type = form.cleaned_data['identity_type']
        p.identity_num = form.cleaned_data['identity_num']
        p.photo = form.cleaned_data['photo']
        p.cellphone = form.cleaned_data['cellphone']
        p.birth_date = form.cleaned_data['birth_date']
        p.address = form.cleaned_data['address']
        p.about = form.cleaned_data['about']
        p.save()
        return super(UserPersonUpdateView, self).form_valid(form)


def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.POST)
        if form.is_valid():
            newpassword = form.cleaned_data['newpassword1']
            username = request.user.username
            password = form.cleaned_data['oldpassword']
            user = authenticate(username=username, password=password)
            if user is not None:
                user.set_password(newpassword)
                user.save()
                user = authenticate(username=username, password=newpassword)
                login(request, user)
                messages.success(request, "Contraseña cambiada exitosamente")
                return HttpResponseRedirect(reverse("backend:user_profile"))

            else:
                messages.warning(request, "Contraseña anterior errada!")
                return render(request, 'auths/user/reset_password.html', {
                    'error': 'You have entered wrong old password', 'form': form})

        else:
            messages.warning(request, "Las contraseñas ingresadas no tienen relación")
            return render(request, 'auths/user/reset_password.html', {
                'error': 'You have entered old password', 'form': form})
    else:
        form = PasswordChangeCustomForm()
    # content = RequestContext(request, {'form': form})
    return render(request, 'auths/user/reset_password.html', {'form': form},)


class UserActivateTemplateView(generic.TemplateView):
    # template_name = "TEMPLATE_NAME"

    def get(self, request, *args, **kwargs):
        u = User.objects.get(id=self.kwargs['pk'])
        if u.is_active:
            u.is_active = False
            u.save()
        else:
            u.is_active = True
            u.save()
        return HttpResponseRedirect(reverse("backend:user_list"))

# class UserCreateView(generic.CreateView):
#     u"""Crea usuario."""

#     model = User
#     template_name = "auths/user/form.html"
#     form_class = UserForm
#     success_url = reverse_lazy("backend:user_list")

#     def get_context_data(self, **kwargs):
#         context = super(UserCreateView, self).get_context_data(**kwargs)
#         return context

#     def form_valid(self, form):
#         self.object = form.save(commit=True)
#         form.cleaned_data['grupo'].user_set.add(self.object)

#         return super(UserCreateView, self).form_valid(form)
