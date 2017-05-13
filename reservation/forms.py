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
  tags = forms.CharField(label='Tags', max_length=500, required=False)

  class Meta:
    model = Resource
    fields = ['name', 'start_time', 'end_time', 'capacity', 'image', 'description']
    error_messages={
      'capacity': {
         'invalid':'Capacity must be > 0.'
       },
    }

  def clean(self):
    cleaned_data = super(ResourceForm, self).clean()
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
# EditResourceForm
#
class EditResourceForm(ResourceForm):
  class Meta(ResourceForm.Meta):
    exclude = ['capacity']

#
# ReservationForm
#
class ReservationForm(ModelForm):
  duration = forms.IntegerField(validators=[validate_duration],
    error_messages={'invalid':'Duration must be > 0.'})

  class Meta:
    model = Reservation
    fields = ['start_time']

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

  start_time = forms.DateTimeField(label='Start Time', required=False)

  duration = forms.IntegerField(validators=[validate_duration],
    error_messages={'invalid':'Enter a valid duration in minutes.'}, required=False)

  def clean(self):
    cleaned_data = super(SearchForm, self).clean()
    start_time = cleaned_data.get("start_time")
    duration = cleaned_data.get("duration")

    if start_time and not duration or duration and not start_time:
      raise ValidationError(
          _('Start time and duration must be supplied together.'),
          code='invalid'
        )
    
    return cleaned_data
