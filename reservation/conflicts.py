from .models import Resource, Reservation
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

#
# Conflict
#
class Conflict():
  def __init__(self, conflicting_reservations, val_error):
    self.conflicting_reservations = conflicting_reservations
    self.val_error = val_error

def get_conflicting_reservations(new_reservation, reservation_list):
  start_time = new_reservation.start_time
  end_time = new_reservation.end_time

  conflicts_list = []

  for reservation in reservation_list:
    existing_start_time = reservation.start_time
    existing_end_time = reservation.end_time
    
    # error: start time appears in existing reservation slot
    if start_time >= existing_start_time and start_time <= existing_end_time:
      conflicts_list.append(reservation)
      continue

    # error: end time appears in existing reservation slot
    if end_time >= existing_start_time and end_time <= existing_end_time:
      conflicts_list.append(reservation)
      continue

    # error: reservation encompasses old reservation
    if start_time < existing_start_time and end_time > existing_end_time:
      conflicts_list.append(reservation)
      continue

  return conflicts_list

def get_conflicts(new_reservation):
  start_time = new_reservation.start_time
  end_time = new_reservation.end_time

  resource = new_reservation.resource
  conflict_list = []
  
  # 1. Check if reservation in resource availability window
  # error: start time not in resource availability window
  if start_time < resource.start_time or start_time > resource.end_time:
    conflict_list.append(Conflict([], ValidationError(
      _('Start time outside resource availability window.'),
      code='invalid')))

  # error: end time not in resource availability window
  # <= : reservation must be at least 1 minute
  if end_time <= resource.start_time or end_time > resource.end_time:
    conflict_list.append(Conflict([], ValidationError(
      _('End time outside resource availability window.'),
      code='invalid')))

  # 2. Check that user doesn't have another reservation that conflicts with this time slot (self-conflict)
  user_reservations = Reservation.objects.filter(owner=new_reservation.owner).exclude(resource=resource)
  self_conflicts_list = get_conflicting_reservations(new_reservation, user_reservations)
  if len(self_conflicts_list) > 0:
    conflict_list.append(Conflict(self_conflicts_list, ValidationError(
      _('You have an existing reservation that conflicts with this time slot.'),
      code='invalid')))

  # 3. Check reservation doesn't conflict with other reservations for this resource
  existing_reservations = Reservation.objects.filter(resource=resource)
  resource_conflicts_list = get_conflicting_reservations(new_reservation, existing_reservations)
  
  if len(resource_conflicts_list) >= resource.capacity:
    conflict_list.append(Conflict(resource_conflicts_list, ValidationError(
      _('Resource is at max capacity for provided time slot.'),
      code='invalid')))
 
  return conflict_list
