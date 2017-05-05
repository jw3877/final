from django.shortcuts import render
#from django.http import HttpResponse

from .models import Resource


def index(request):
  resource_list = Resource.objects.order_by('-start_time')
  context = {'resource_list': resource_list}
  return render(request, 'reservation/index.html', context)

def create(request):
  return render(request, 'reservation/create.html')
