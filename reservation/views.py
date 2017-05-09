from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from .models import Resource, Reservation, Tag
from .forms import ResourceForm, ReservationForm, UserForm, ResourceTagForm
from django.db.models import Q
from django.contrib.auth import authenticate, login


#from django.contrib.admin import widgets

def addResourceTags(tags, resource):
  tagNameList = tags.split()
  
  for tagName in tagNameList:
    # check if tag already exists
    if Tag.objects.filter(name=tagName).exists():
      existing_tags = Tag.objects.filter(name=tagName)
      for tag in existing_tags:
        tag.resources.add(resource)

    # tag doesn't already exist
    else:
      new_tag = Tag(name=tagName)
      new_tag.save()
      new_tag.resources.add(resource)
    

#
# index
#
def index(request):
  all_resources = Resource.objects.order_by('-start_time')

  if request.user.is_authenticated:
    current_time = datetime.now()
    user_resources = Resource.objects.filter(owner=request.user).order_by('start_time')
    user_reservations = Reservation.objects.filter(owner=request.user).order_by('start_time')

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
  current_time = datetime.now()
  resource = get_object_or_404(Resource, pk=resource_id)
  reservation_list = Reservation.objects.filter(resource=resource)
  total_reservations = reservation_list.count()
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
    resource_form = ResourceTagForm(request.POST)
    if resource_form.is_valid():
      new_resource = resource_form.save(commit=False)
      new_resource.owner = request.user
      tags = resource_form.cleaned_data['tags']
      new_resource.save()
      addResourceTags(tags, new_resource)
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
  
  if reservation.owner != request.user:
    return HttpResponseForbidden()
  
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


