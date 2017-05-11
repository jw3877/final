from django.contrib.syndication.views import Feed
from .models import Resource, Reservation

class ResourceFeed(Feed):

  def get_object(self, request, resource_id):
    return Resource.objects.get(pk=resource_id)

  def title(self, obj):
    return "Reservations for %s" % obj.name

  def link(self, obj):
    return obj.get_absolute_url()

  def description(self, obj):
    return "Reservations recently made for resource: %s" % obj.name

  def items(self, obj):
    return Reservation.objects.filter(resource=obj).order_by('start_time')

  def item_description(self, obj):
    return 'A {0} minute reservation that begins at {1} and ends at {2}.'.format(obj.duration(), obj.start_time.strftime('%m-%d-%Y %H:%M %Z'), obj.end_time.strftime('%m-%d-%Y %H:%M %Z'))

  def item_author_name(self, obj):
    return obj.owner.username

  def item_author_email(self, obj):
    return obj.owner.email

