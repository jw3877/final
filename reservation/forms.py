from .models import Resource, Reservation
from django.contrib.auth.models import User
from django.forms import ModelForm, extras, Form
from django import forms
from .validators import validate_duration
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta
from django.utils import timezone


#
# ResourceForm
#
class ResourceForm(ModelForm):
  class Meta:
    model = Resource
    fields = ['name', 'start_time', 'end_time']

#
# ResourceTagForm
#
class ResourceTagForm(ResourceForm):
  tags = forms.CharField(label='Tags', max_length=500, required=False)

  def clean(self):
    cleaned_data = super(ResourceTagForm, self).clean()
    start_time = cleaned_data.get("start_time")
    end_time = cleaned_data.get("end_time")

    recent_time = timezone.now() - timedelta(minutes=1)
    
    if start_time and end_time:
      # start time must be within 1 minute of current time
      if start_time < recent_time:
        raise ValidationError(
          _('Start time cannot be in the past.'),
          code='invalid'
        )

      # end time must come after start time
      if start_time >= end_time:
        raise ValidationError(
          _('Start time must come before end time.'),
          code='invalid'
        )
        
    return cleaned_data

#
# ReservationForm
#
class ReservationForm(ModelForm):
  class Meta:
    model = Reservation
    fields = ['start_time']

#
# ReservationDurationForm
#
class ReservationDurationForm(ReservationForm):
  duration = forms.IntegerField(validators=[validate_duration],
    error_messages={'invalid':'Enter a valid duration in minutes.'})

#
# UserForm
#
class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password']
    widgets = { 
      'password': forms.PasswordInput(),
    }

#
# SearchForm
#
class SearchForm(Form):
  name = forms.CharField(label='Name Contains', max_length=500, required=False)
