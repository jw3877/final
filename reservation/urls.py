from django.conf.urls import url, include
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # ex: /resource/create/
    url(r'^resource/create/$', views.createResource, name='createResource'),
    
    # ex: /resource/5/
    url(r'^resource/(?P<resource_id>[0-9]+)/$', views.resource, name='resource'),\

    # ex: /resource/5/reserve/
    url(r'^resource/(?P<resource_id>[0-9]+)/reserve/$', views.createReservation, name='createReservation'),

    # ex: /resource/5/edit/
    url(r'^resource/(?P<resource_id>[0-9]+)/edit/$', views.editResource, name='editResource'),

    # ex: /reservation/5/
    url(r'^reservation/(?P<reservation_id>[0-9]+)/$', views.reservation, name='reservation'),

    # auth
    url('^', include('django.contrib.auth.urls')),

]
