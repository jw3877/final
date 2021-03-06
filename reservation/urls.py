from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from .feed import ResourceFeed
from django.conf import settings
from django.conf.urls.static import static


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

    # ex: /resource/5/rss/
    url(r'^resource/(?P<resource_id>[0-9]+)/rss/$', ResourceFeed(), name='rss'),

    # ex: /reservation/5/
    url(r'^reservation/(?P<reservation_id>[0-9]+)/$', views.reservation, name='reservation'),

    # ex: /reservation/5/delete/
    url(r'^reservation/(?P<reservation_id>[0-9]+)/delete/$', views.deleteReservation, name='deleteReservation'),

    # ex: /user/name/
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.user, name='user'),

    # ex: /tag/name/
    url(r'^tag/(?P<tagname>[A-Za-z0-9]+)/$', views.tag, name='tag'),

    # ex: /register/
    url(r'^register/$', views.createUser, name='createUser'),

    # ex: /search/
    url(r'^search/$', views.search, name='search'),

    # auth
    url('^', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
