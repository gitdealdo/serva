from django.conf.urls import url

from backend_apps.auths.views.menu import MenuUpdateActiveView, \
    MenuUpdateView, MenuDeleteView
from .views import user
from .views.menu import (MenuListView, MenuCreateView)
from .views.permission import PermissionCreateView,\
    PermissionDeleteView, PermissionListView, PermissionUpdateView

urlpatterns = [

    # User
    url(r'^user/list/$', user.UserListView.as_view(), name='user_list'),
    url(r'^user/create/$', user.UserPersonCreateView.as_view(),
        name='user_person_create'),
    url(r'^user/(?P<pk>[^/]+)/delete/$', user.UserDeleteView.as_view(),
        name='user_delete'),
    url(r'^user/perfil/$', user.UserTemplateView.as_view(),
        name='user_profile'),
    url(r'^user/(?P<pk>[^/]+)/update/$', user.UserPersonUpdateView.as_view(),
        name='user_update'),
    url(r'^user/change_password/$', user.change_password, name='change_password'),
    url(r'^user/(?P<pk>[^/]+)/activate/$',
        user.UserActivateTemplateView.as_view(), name='user_activate'),
    url(r'^user/change_theme/$',
        user.change_user_theme, name='change_user_theme'),

    # Menu
    url(r'^menu/list/$', MenuListView.as_view(), name='menu_list'),
    url(r'^menu/add/$', MenuCreateView.as_view(), name='menu_add'),
    url(r'^menu/state/(?P<state>[\w\d\-]+)/(?P<pk>[^/]+)/$',
        MenuUpdateActiveView.as_view(), name='menu_state'),
    url(r'^menu/update/(?P<pk>[^/]+)/$',
        MenuUpdateView.as_view(), name='menu_update'),
    url(r'^menu/delete/(?P<pk>[^/]+)/$',
        MenuDeleteView.as_view(), name='menu_delete'),

    #
    url(r'^permission/delete/(?P<pk>.*)/$',
        PermissionDeleteView.as_view(), name='permission_delete'),  # x pony
    url(r'^permission/update/(?P<pk>.*)/$',
        PermissionUpdateView.as_view(), name='permission_update'),
    url(r'^permission/add/$',
        PermissionCreateView.as_view(), name='permission_add'),
    url(r'^permission/list/$',
        PermissionListView.as_view(), name='permission_list'),


]
