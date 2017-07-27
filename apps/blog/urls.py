from django.conf.urls import url

from .views.post import (
    PostListView, PostCreateView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    # post
    url(r'^post/listar/$', PostListView.as_view(), name='post_list'),
    url(r'^post/crear/', PostCreateView.as_view(), name='post_add'),
    url(r'^post/actualizar/(?P<pk>[^/]+)$', PostUpdateView.as_view(), name='post_update'),
    url(r'^post/eliminar/(?P<pk>[^/]+)$', PostDeleteView.as_view(), name='post_delete'),

    # Comment
    # url(r'^post/lisart/$', PostListView.as_view(), name='post_list'),
    # url(r'^post/crear/', PostListView.as_view(), name='post_add'),
    # url(r'^post/actualizar/$', PostListView.as_view(), name='post_update'),
    # url(r'^post/eliminar/$', PostListView.as_view(), name='post_delete'),
]
