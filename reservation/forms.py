from django.forms import ModelForm
from .models import Resource
from django.forms import extras



class ResourceForm(ModelForm):
  class Meta:
    model = Resource
    fields = ['name', 'start_time', 'end_time']
