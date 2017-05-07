from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


#from django.contrib.admin import widgets

from .models import Resource
from .forms import ResourceForm

def index(request):
  resource_list = Resource.objects.order_by('-start_time')
  context = {
    'resource_list': resource_list,
    'user_resource_list': []
  }

  if request.user.is_authenticated:
    user_resource_list = Resource.objects.filter(owner=request.user)
    context['user_resource_list'] = user_resource_list

  return render(request, 'reservation/index.html', context)

def detail(request, resource_id):
    return HttpResponse("You're looking at resource %s." % resource_id)

@login_required
def create(request):
  if request.method == 'POST':
    f = ResourceForm(request.POST)
    new_resource = f.save(commit=False)
    new_resource.owner = request.user
    new_resource.save()
    return HttpResponseRedirect(reverse('index'))
    
  resource_form = ResourceForm()
  context = {'resource_form': resource_form}
  return render(request, 'reservation/create.html', context)
