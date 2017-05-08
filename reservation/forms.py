from .models import Resource, Reservation
from django.contrib.auth.models import User
from django.forms import ModelForm, extras, Form
from django import forms




class ResourceForm(ModelForm):
  class Meta:
    model = Resource
    fields = ['name', 'start_time', 'end_time']

class ReservationForm(ModelForm):
  class Meta:
    model = Reservation
    fields = ['start_time', 'duration']

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
    widgets = { 
      'password': forms.PasswordInput(),
    }
