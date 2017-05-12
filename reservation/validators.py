from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

def validate_duration(value):
  if value < 1:
    raise ValidationError(
      _('Invalid duration: %(value)s'),
      code='invalid',
      params={'value': value},
    )

def validate_capacity(value):
  if value < 1:
    raise ValidationError(
      _('Invalid capacity: %(value)s'),
      code='invalid',
      params={'value': value},
    )
