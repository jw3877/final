from django.utils import timezone
from .models import Resource, Reservation, Tag
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element, tostring
from datetime import timedelta

def get_date_format():
  return '%A, %B %d, %Y @ %I:%M %p'

def add_resource_tags(tags, resource):
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

def get_user_reservations(user):
  current_time = timezone.now()
  return Reservation.objects.filter(owner=user, end_time__gte=current_time).order_by('start_time')
    

def get_resource_reservations(resource):
  current_time = timezone.now()
  return Reservation.objects.filter(resource=resource, end_time__gte=current_time).order_by('start_time')

def total_reservation_conflicts(new_reservation, reservation_list):
  start_time = new_reservation.start_time
  end_time = new_reservation.end_time

  total_conflicts = 0

  for reservation in reservation_list:
    existing_start_time = reservation.start_time
    existing_end_time = reservation.end_time
    
    # error: start time appears in existing reservation slot
    if start_time >= existing_start_time and start_time <= existing_end_time:
      total_conflicts += 1
      continue

    # error: end time appears in existing reservation slot
    if end_time >= existing_start_time and end_time <= existing_end_time:
      total_conflicts += 1
      continue

    # error: reservation encompasses old reservation
    if start_time < existing_start_time and end_time > existing_end_time:
      total_conflicts += 1
      continue

  return total_conflicts

def validate_reservation(new_reservation):
  start_time = new_reservation.start_time
  end_time = new_reservation.end_time

  resource = new_reservation.resource
  
  # 1. Check if reservation in resource availability window
  # error: start time not in resource availability window
  if start_time < resource.start_time or start_time > resource.end_time:
    return ValidationError(
      _('Start time outside resource availability window.'),
      code='invalid'
    )

  # error: end time not in resource availability window
  # <= : reservation must be at least 1 minute
  if end_time <= resource.start_time or end_time > resource.end_time:
    return ValidationError(
      _('End time outside resource availability window.'),
      code='invalid'
    )

  # 2. Check that user doesn't have another reservation that conflicts with this time slot (self-conflict)
  user_reservations = Reservation.objects.filter(owner=new_reservation.owner)
  self_conflicts = total_reservation_conflicts(new_reservation, user_reservations)
  if self_conflicts > 0:
    return ValidationError(
      _('You have an existing reservation that conflicts with this time slot.'),
      code='invalid'
    )

  # 3. Check reservation doesn't conflict with other reservations for this resource
  existing_reservations = Reservation.objects.filter(resource=resource)
  total_conflicts = total_reservation_conflicts(new_reservation, existing_reservations)
  
  if total_conflicts >= resource.capacity:
    return ValidationError(
      _('Resource is at max capacity for provided time slot.'),
      code='invalid'
    )
 
  return None

def get_search_results(name, start_time, duration):
  results_list = []

  if name and start_time and duration:
    end_time = start_time + timedelta(minutes=duration)
    results_list = Resource.objects.filter(name__contains=name, start_time__lte=start_time, end_time__gte=end_time)

  elif start_time and duration:
    end_time = start_time + timedelta(minutes=duration)
    results_list = Resource.objects.filter(start_time__lte=start_time, end_time__gte=end_time)

  elif name:
    results_list = Resource.objects.filter(name__contains=name)

  return results_list

def email_user_reservation_confirmed(reservation):
  date_format = get_date_format()

  subject = 'Reservation Confirmed on Open Resource'
  message = '''The following reservation has been confirmed:

           Resource: {0}
           Start Time: {1}
           End Time: {2}
           Duration: {3} minutes
           
           Thank you for choosing Open Resource. We hope to see you back again soon!
           
           Sincerely,
           The Management'''.format(reservation.resource.name, reservation.start_time.strftime(date_format), reservation.end_time.strftime(date_format), reservation.duration())
  reservation.owner.email_user(subject, message)


