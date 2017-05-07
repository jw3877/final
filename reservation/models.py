from django.db import models
from django.contrib.auth.models import User

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

# set of tags that describe the type of resource
class Tag(models.Model):
  name = models.CharField(max_length=200)
  resources = models.ManyToManyField(Resource)

  def __str__(self):
    return self.name
