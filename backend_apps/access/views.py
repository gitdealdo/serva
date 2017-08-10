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
