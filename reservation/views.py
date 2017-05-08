from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from .models import Resource, Reservation
from .forms import ResourceForm, ReservationForm
from django.db.models import Q

#from django.contrib.admin import widgets

#
# index
#
def index(request):
  all_resources = Resource.objects.order_by('-start_time')

  if request.user.is_authenticated:
    current_time = datetime.now()
    user_resources = Resource.objects.filter(owner=request.user).order_by('start_time')
    user_reservations = Reservation.objects.order_by('start_time')

  else:
    user_resources = []
    user_reservations = []

  context = {
    'all_resources': all_resources,
    'user_resources': user_resources,
    'user_reservations': user_reservations
  }

  return render(request, 'reservation/index.html', context)

#
# user
# 
def user(request, username):
  user = get_object_or_404(User, username=username)
  user_reservations = Reservation.objects.filter(owner=user)
  user_resources = Resource.objects.filter(owner=user)
  context = {
    'user_reservations': user_reservations,
    'user_resources': user_resources,
    'username': username
  }

  return render(request, 'reservation/user.html', context)

#
# resource
#
def resource(request, resource_id):
  current_time = datetime.now()
  resource = get_object_or_404(Resource, pk=resource_id)
  reservation_list = Reservation.objects.filter(resource=resource)
  context = {
    'resource': resource,
    'reservation_list': reservation_list
  }
  return render(request, 'reservation/resource.html', context)

#
# reservation
#
def reservation(request, reservation_id):
  reservation = get_object_or_404(Reservation, pk=reservation_id)
  context = {
    'reservation': reservation
  }
  return render(request, 'reservation/reservation.html', context)

#
# createResource
#
@login_required
def createResource(request):
  if request.method == 'POST':
    resource_form = ResourceForm(request.POST)
    if resource_form.is_valid():
      new_resource = f.save(commit=False)
      new_resource.owner = request.user
      new_resource.save()
      return HttpResponseRedirect(reverse('index'))
    
  else:
    resource_form = ResourceForm()

  return render(request, 'reservation/createResource.html', {'resource_form': resource_form})

#
# createReservation
#
@login_required
def createReservation(request, resource_id):
  resource = get_object_or_404(Resource, pk=resource_id)

  if request.method == 'POST':
    reservation_form = ReservationForm(request.POST)
    if reservation_form.is_valid():
      new_reservation = reservation_form.save(commit=False)
      new_reservation.resource = resource
      new_reservation.owner = request.user
      new_reservation.save()
      return HttpResponseRedirect(reverse('index'))

  else:
    reservation_form = ReservationForm()
    
  context = {
    'reservation_form': reservation_form,
    'resource': resource
  }

  return render(request, 'reservation/createReservation.html', context)

#
# deleteReservation
#
@login_required
def deleteReservation(request, reservation_id):
  reservation = get_object_or_404(Reservation, pk=reservation_id)
  
  if request.method == 'POST':
    reservation.delete()
    return redirect('index')

  context = {
    'reservation': reservation
  }

  return render(request, 'reservation/confirmDeleteReservation.html', context)

#
# editResource
#
@login_required
def editResource(request, resource_id):
  resource = get_object_or_404(Resource, pk=resource_id)

  if request.method == 'POST':
    resource_form = ResourceForm(request.POST, instance=resource)
    if resource_form.is_valid():
      resource_form.save()
      return redirect('resource', resource.id)

  else:
    resource_form = ResourceForm(instance=resource)

  context = {
    'resource_form': resource_form,
    'resource': resource
  }

  return render(request, 'reservation/editResource.html', context)


