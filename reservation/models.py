from django.db import models
from django.contrib.auth.models import User

#
# Resource
#
class Resource(models.Model):
  # name of the resource
  name = models.CharField(max_length=200)

  # owner of the resource
  owner = models.ForeignKey(User)

  # availability hours (will be any two times within the same day, e.g. 9am - 5pm)
  start_time = models.DateTimeField('available start time')
  end_time = models.DateTimeField('availabile end time')

  def __str__(self):
    return self.name

#
# Reservation
#
class Reservation(models.Model):
  # reservation hours (will be any two times within the same day, e.g. 9am - 5pm)
  start_time = models.DateTimeField('reservation start time')
  end_time = models.DateTimeField('availabile end time')
  
  # resource that has been reserved
  resource = models.ForeignKey(Resource)

  # owner of the reservation
  owner = models.ForeignKey(User)

  def __str__(self):
    return self.resource

  def duration(self):
    d = self.end_time - self.start_time
    return int(d.total_seconds() / 60)

#
# Tag
#
class Tag(models.Model):
  name = models.CharField(max_length=200, unique=True)
  resources = models.ManyToManyField(Resource)

  def __str__(self):
    return self.name


