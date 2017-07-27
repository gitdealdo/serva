from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
# from django.core.urlresolvers import reverse_lazy
# from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render
# from ..forms.RegistroForm import RegistroForm
from .forms import UserLoginForm


def logout_view(request):
    logout(request)
    return redirect("/")


def login_view(request):
    context = {}
    context['title'] = "Login"
    context['nombre'] = "ServA"
    context['lema'] = "Nutrición UPeU"
    context['form'] = UserLoginForm(request.POST or None)
    if context['form'].is_valid():
        username = context['form'].cleaned_data.get("username")
        password = context['form'].cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        msg = "Bienvenido sr(*): %s, ¡Empecemos! " % (username)
        messages.success(request, msg)

        # Roles estaticos estudiante y administrador

        return redirect("/")

    return render(request, "access/login.html", context)

# class RegistroCreateView(CreateView):
#     u"""Crea usuario."""

#     template_name = "register.html"
#     model = User
#     form_class = RegistroForm
#     success_url = reverse_lazy("cuenta:login")

#     def get_context_data(self, **kwargs):
#         context = super(RegistroCreateView,
#                         self).get_context_data(**kwargs)
#         context['testimonios'] = Testimonio.objects.filter(estado=True)
#         return context

#     def form_valid(self, form):
#         self.object = form.save(commit=True)
#         print("registro create view")
#         print(form.cleaned_data["email"])
#         person = Persona(
#             usuario=self.object,
#             nombre=form.cleaned_data['nombre'],
#             apellido=form.cleaned_data['apellido'],
#             correo=form.cleaned_data['email'],
#             telefono=form.cleaned_data['telefono'],
#             pais=form.cleaned_data['pais'],
#             ciudad=form.cleaned_data['ciudad'],
#             direccion=form.cleaned_data['direccion'],

#         )

#         user = authenticate(username=self.request.POST[
#             'username'], password=self.request.POST['password1'])

#         user_c = User.objects.get(username=user.username)
#         grupo = Group.objects.get(name=ESTUDIANTE)
#         grupo.user_set.add(user_c)
#         if user is not None:
#             login(self.request, user)
#         # this is the only time the user would be logged in.

#         person.save()
#         return super(RegistroCreateView, self).form_valid(form)


# def home(request):
#     title = "Home"
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         messages.success(request, "Bienvenido sr(ta) %s" % user)
#         return redirect("/")

# return render(request, "access/home.html", {'form': form, "title":
# title})
