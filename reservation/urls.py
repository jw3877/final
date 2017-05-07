from django.conf.urls import url, include
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    
    # ex: /resource/5/
    url(r'^resource/(?P<resource_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^accounts/login/$', auth_views.LoginView.as_view()),

    # auth
    url('^', include('django.contrib.auth.urls')),

]
