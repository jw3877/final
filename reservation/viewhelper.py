from django.utils import timezone
from .models import Resource, Reservation, Tag
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


