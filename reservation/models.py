from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

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

  # max_length not enforced in db, only in Textarea widget of form field
  description = models.TextField('description', max_length=300, blank=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    from . import views
    return reverse('resource', args=[str(self.id)])

  def expired(self):
    return self.end_time <= timezone.now()

  def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

  # image associated with resource
  image = models.ImageField(upload_to=user_directory_path, default='resource.png')

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
    return "Reservation (id: {})".format(self.id)

  def get_absolute_url(self):
    from . import views
    return reverse('reservation', args=[str(self.id)])

  def duration(self):
    d = self.end_time - self.start_time
    return int(d.total_seconds() / 60)

#
# Tag
#
class Tag(models.Model):
  name = models.CharField(max_length=100, unique=True)
  resources = models.ManyToManyField(Resource)

  def __str__(self):
    return self.name

#
# Counter
#
class Counter(models.Model):
  resource = models.ForeignKey(Resource)
  count = models.BigIntegerField(default=0)



