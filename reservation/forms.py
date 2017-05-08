from django.forms import ModelForm, extras, Form
from .models import Resource, Reservation



class ResourceForm(ModelForm):
  class Meta:
    model = Resource
    fields = ['name', 'start_time', 'end_time']

class ReservationForm(ModelForm):
  class Meta:
    model = Reservation
    fields = ['start_time', 'duration']
