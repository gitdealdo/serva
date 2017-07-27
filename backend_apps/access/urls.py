from django.conf.urls import url

from .views import (logout_view, login_view)

urlpatterns = [
    # url(r'^registro/$',
    #     RegistroCreateView.as_view(), name='register'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),

]
