from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^callback/$', views.callback, name='callback'),
    url(r'^login/$', views.login, name='login'),
    url(r'^api/v1/playlists/(?P<playlist_id>(\d{1,3}))/$', views.playlists, name='playlists'),
    url(r'^api/v1/playlists/$', views.playlists, name='playlists'),
    url(r'^visualizations/$', views.visualizations, name='visualizations'),
    url(r'^refresh_token/$', views.refresh_token, name='refresh_token'),
]
