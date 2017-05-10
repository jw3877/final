from django.utils import timezone
from .models import Resource, Reservation, Tag
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

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

def reservation_conflict(new_reservation, reservation_list):
  start_time = new_reservation.start_time
  end_time = new_reservation.end_time

  resource = new_reservation.resource

  # error: start time not in available resource window
  if start_time < resource.start_time or start_time > resource.end_time:
    return ValidationError(
      _('Start time outside resource availability window.'),
      code='invalid'
    )

  # error: end time not in available resource window
  # <= : reservation must be at least 1 minute
  if end_time <= resource.start_time or end_time > resource.end_time:
    return ValidationError(
      _('End time outside resource availability window.'),
      code='invalid'
    )

  for reservation in reservation_list:
    existing_start_time = reservation.start_time
    existing_end_time = reservation.end_time
    
    # error: start time appears in existing reservation slot
    if start_time >= existing_start_time and start_time <= existing_end_time:
      return ValidationError(
        _('Start time conflicts with existing reservation.'),
        code='invalid'
      )

    # error: end time appears in existing reservation slot
    if end_time >= existing_start_time and end_time <= existing_end_time:
      return ValidationError(
        _('End time conflicts with existing reservation.'),
        code='invalid'
      )

    # error: reservation encompasses old reservation
    if start_time < existing_start_time and end_time > existing_end_time:
      return ValidationError(
        _('Reservation encompasses existing reservation.'),
        code='invalid'
      )

  return None
