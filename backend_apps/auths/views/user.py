from django.views.generic.list import ListView

from ..models import User


class UserListView(ListView):
    model = User
    template_name = "auths/user/list.html"


