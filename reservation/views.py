from django.shortcuts import render, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime




#from django.contrib.admin import widgets

from .models import Resource, Reservation
from .forms import ResourceForm, ReservationForm

def index(request):
  resource_list = Resource.objects.order_by('-start_time')
  context = {
    'resource_list': resource_list,
    'user_resource_list': []
  }

  if request.user.is_authenticated:
    user_resource_list = Resource.objects.filter(owner=request.user).order_by('start_time')
    context['user_resource_list'] = user_resource_list

  return render(request, 'reservation/index.html', context)

def resource(request, resource_id):
  current_time = datetime.now()
  requested_resource = get_object_or_404(Resource, pk=resource_id)
  reservations_list = Reservation.objects.filter(resource=requested_resource)
  context = {
    'resource': requested_resource,
    'reservations_list': reservations_list
  }
  return render(request, 'reservation/resource.html', context)

def reservation(request, reservation_id):
  requested_reservation = get_object_or_404(Reservation, pk=reservation_id)
  context = {
    'reservation': requested_reservation
  }
  return render(request, 'reservation/reservation.html', context)


@login_required
def createResource(request):
  if request.method == 'POST':
    f = ResourceForm(request.POST)
    new_resource = f.save(commit=False)
    new_resource.owner = request.user
    new_resource.save()
    return HttpResponseRedirect(reverse('index'))
    
  resource_form = ResourceForm()
  context = {'resource_form': resource_form}
  return render(request, 'reservation/createResource.html', context)

@login_required
def createReservation(request, resource_id):
  resource = get_object_or_404(Resource, pk=resource_id)

  if request.method == 'POST':
    f = ReservationForm(request.POST)
    new_reservation = f.save(commit=False)
    new_reservation.resource = resource
    new_reservation.owner = request.user
    
    if new_reservation.duration <= 0:
      reservation_form = ReservationForm(request.POST)
      context = {
        'reservation_form': reservation_form,
        'error_message': 'duration must be at least 1 minute',
        'resource': resource
      }
      return render(request, 'reservation/createReservation.html', context)

    new_reservation.save()
    return HttpResponseRedirect(reverse('index'))
  reservation_form = ReservationForm()
  context = {
    'reservation_form': reservation_form,
    'resource': resource
  }
  return render(request, 'reservation/createReservation.html', context)


