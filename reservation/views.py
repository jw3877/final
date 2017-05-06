from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


#from django.contrib.admin import widgets

from .models import Resource
from .forms import ResourceForm

def index(request):
  resource_list = Resource.objects.order_by('-start_time')
  context = {'resource_list': resource_list}
  return render(request, 'reservation/index.html', context)

def detail(request, resource_id):
    return HttpResponse("You're looking at resource %s." % resource_id)

def create(request):
  if request.method == 'POST':
    f = ResourceForm(request.POST)
    new_resource = f.save()
    return HttpResponseRedirect(reverse('index'))
    
  resource_form = ResourceForm()
  context = {'resource_form': resource_form}
  return render(request, 'reservation/create.html', context)
