from .models import Resource, Reservation
from django.contrib.auth.models import User
from django.forms import ModelForm, extras, Form
from django import forms
from .validators import validate_duration
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _




class ResourceForm(ModelForm):
  class Meta:
    model = Resource
    fields = ['name', 'start_time', 'end_time']

class ReservationForm(ModelForm):
  class Meta:
    model = Reservation
    fields = ['start_time']

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password']
    widgets = { 
      'password': forms.PasswordInput(),
    }

class ResourceTagForm(ResourceForm):
  tags = forms.CharField(label='Tags', max_length=500, required=False)

  def clean(self):
    cleaned_data = super(ResourceTagForm, self).clean()
    start_time = cleaned_data.get("start_time")
    end_time = cleaned_data.get("end_time")

    if start_time and end_time:
      if start_time >= end_time:
        raise ValidationError(
          _('Start time must come before end time.'),
          code='invalid'
        )
        
    return cleaned_data

class ReservationDurationForm(ReservationForm):
  duration = forms.IntegerField(validators=[validate_duration],
    error_messages={'invalid':'Enter a valid duration.'})
