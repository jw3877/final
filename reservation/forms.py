from django.forms import ModelForm
from .models import Resource, Reservation
from django.forms import extras



class ResourceForm(ModelForm):
  class Meta:
    model = Resource
    fields = ['name', 'start_time', 'end_time']

class ReservationForm(ModelForm):
  class Meta:
    model = Reservation
    fields = ['start_time', 'duration']
