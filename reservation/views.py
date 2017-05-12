from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import Resource, Reservation, Tag, Counter
from .viewhelper import get_user_reservations, get_resource_reservations, add_resource_tags, validate_reservation, get_search_results, email_user_reservation_confirmed
from .forms import ResourceForm, ReservationForm, UserForm, ResourceTagForm, ReservationDurationForm, SearchForm

from datetime import datetime, timedelta
from django.db.models import F
from django.contrib import messages

#
# index
#
def index(request):
  all_resources = Resource.objects.order_by('-start_time')

  if request.user.is_authenticated:
    user_resources = Resource.objects.filter(owner=request.user).order_by('start_time')
    user_reservations = get_user_reservations(request.user)

    #user_resources = []
    #for reservation in user_reservations:
      #if reservation.resource not in user_resources:
        #user_resources.append(reservation.resource)
    

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
  user_reservations = get_user_reservations(user)
  user_resources = Resource.objects.filter(owner=user)
  context = {
    'user_reservations': user_reservations,
    'user_resources': user_resources,
    'username': username
  }

  return render(request, 'reservation/user.html', context)

#
# tag
# 
def tag(request, tagname):
  tag = get_object_or_404(Tag, name=tagname)
  resource_list = tag.resources.all()
  context = {
    'resource_list': resource_list,
    'tagName': tag.name 
  }

  return render(request, 'reservation/tag.html', context)

#
# createUser
#
def createUser(request):
  if request.user.is_authenticated:
      return HttpResponseRedirect(reverse('index'))

  if request.method == 'POST':
    registration_form = UserForm(request.POST)
    
    if registration_form.is_valid():
      username = request.POST['username']
      password = request.POST['password']
      email = request.POST['email']

      user = User.objects.create_user(username, email, password)

      # login user after account is created
      authenticated_user = authenticate(username=username, password=password)

      if authenticated_user is not None:
        login(request, authenticated_user)
        return HttpResponseRedirect(reverse('index'))

      else:
        return HttpResponseServerError()  
    
  else:
    registration_form = UserForm()

  return render(request, 'reservation/createUser.html', {'registration_form': registration_form})

#
# resource
#
def resource(request, resource_id):
  resource = get_object_or_404(Resource, pk=resource_id)
  reservation_list = get_resource_reservations(resource)
  
  # reservation_list only contains reservations >= currrent_time
  counter, created = Counter.objects.get_or_create(resource=resource)
  total_reservations = counter.count

  tags = resource.tag_set.all()
  context = {
    'resource': resource,
    'reservation_list': reservation_list,
    'total_reservations': total_reservations,
    'tags': tags
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
    resource_form = ResourceTagForm(request.POST, request.FILES)
    if resource_form.is_valid():
      new_resource = resource_form.save(commit=False)
      new_resource.owner = request.user
      tags = resource_form.cleaned_data['tags']
      new_resource.save()
      add_resource_tags(tags, new_resource)
      message = 'Successfully created resource.'
      messages.add_message(request, messages.SUCCESS, message)
      return HttpResponseRedirect(reverse('index'))
    
  else:
    resource_form = ResourceTagForm()

  return render(request, 'reservation/createResource.html', {'resource_form': resource_form})

#
# createReservation
#
@login_required
def createReservation(request, resource_id):
  resource = get_object_or_404(Resource, pk=resource_id)

  # error: resource has expired
  if resource.expired():
    return render(request, 'reservation/resourceExpired.html', {'resource': resource})

  # POST
  if request.method == 'POST':
    reservation_form = ReservationDurationForm(request.POST)
    # form is valid
    if reservation_form.is_valid():
      new_reservation = reservation_form.save(commit=False)
      new_reservation.resource = resource
      new_reservation.owner = request.user
      form_duration = reservation_form.cleaned_data['duration']
      duration = timedelta(minutes=form_duration)
      new_reservation.end_time = reservation_form.cleaned_data['start_time'] + duration
       
      # check for reservation conflict
      val_error = validate_reservation(new_reservation)
     
      # form is valid but reservation conflict
      if val_error is not None:
        reservation_form.add_error(None, val_error)
     
      # form is valid -- no conflict
      else:
        new_reservation.save()

        # update counter -- used to display total # of past reservations
        counter, created = Counter.objects.get_or_create(resource=resource)
        counter.count = F('count') + 1
        counter.save()

        # update resource capacity count
        #resource.capacity = F('capacity') + 1
        #resource.save()
       
        # e-mail user
        email_user_reservation_confirmed(new_reservation)

        message = 'Successfully created reservation.'
        messages.add_message(request, messages.SUCCESS, message)

        return HttpResponseRedirect(reverse('index'))

  # GET
  else:
    reservation_form = ReservationDurationForm()
    
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
  
  if reservation.owner != request.user:
    return HttpResponseForbidden()
  
  if request.method == 'POST':
    reservation.delete()
    message = 'Successfully deleted reservation.'
    messages.add_message(request, messages.SUCCESS, message)
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
    resource_form = ResourceForm(request.POST, request.FILES, instance=resource)
    if resource_form.is_valid():
      resource_form.save()
      message = 'Changes have been saved.'
      messages.add_message(request, messages.SUCCESS, message)
      return redirect('resource', resource.id)

  else:
    resource_form = ResourceForm(instance=resource)

  context = {
    'resource_form': resource_form,
    'resource': resource
  }

  return render(request, 'reservation/editResource.html', context)
 
#
# search
#
def search(request):
  results_list = []
  
  # GET
  if request.method == 'GET':
    search_form = SearchForm(request.GET)
  
    if search_form.is_valid():
      name = search_form.cleaned_data['name']
      start_time = search_form.cleaned_data['start_time']
      duration = search_form.cleaned_data['duration']

      results_list = get_search_results(name, start_time, duration)
 
  # POST
  else:
    search_form = SearchForm()
  
  context = {
    'search_form': search_form,
    'results_list': results_list
  }

  return render(request, 'reservation/search.html', context)

