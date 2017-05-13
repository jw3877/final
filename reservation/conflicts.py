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

#
# get_conflicting_reservations
#
def get_conflicting_reservations(new_reservation, reservation_list):
  start_time = new_reservation.start_time
  end_time = new_reservation.end_time

  conflicts_list = []

  for reservation in reservation_list:
    existing_start_time = reservation.start_time
    existing_end_time = reservation.end_time
    
    # error: start time appears in existing reservation slot
    if start_time >= existing_start_time and start_time < existing_end_time:
      conflicts_list.append(reservation)
      continue

    # error: end time appears in existing reservation slot
    if end_time > existing_start_time and end_time <= existing_end_time:
      conflicts_list.append(reservation)
      continue

    # error: reservation encompasses old reservation
    if start_time < existing_start_time and end_time > existing_end_time:
      conflicts_list.append(reservation)
      continue

  return conflicts_list

#
# get_conflicts
#
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
  global_self_reservations = Reservation.objects.filter(owner=new_reservation.owner)
  global_self_conflicts = get_conflicting_reservations(new_reservation, global_self_reservations)
  total_global_self_conflicts = len(global_self_conflicts)

  if total_global_self_conflicts > 0:
    conflict_list.append(Conflict(global_self_conflicts, ValidationError(
      _('You have an existing reservation that conflicts with the requested time slot.'),
      code='invalid')))

  # 3. Check reservation doesn't conflict with other reservations for this resource
  # filter self conflicts with this resource as we already returned them with global_conflicts
  local_other_reservations = Reservation.objects.filter(resource=resource).exclude(owner=new_reservation.owner)

  local_other_conflicts = get_conflicting_reservations(new_reservation, local_other_reservations)

  local_self_reservations = Reservation.objects.filter(resource=resource, owner=new_reservation.owner)

  local_self_conflicts = get_conflicting_reservations(new_reservation, local_self_reservations)

  total_local_other_conflicts = len(local_other_conflicts)
  total_local_self_conflicts = len(local_self_conflicts)
  total_local_conflicts = total_local_other_conflicts + total_local_self_conflicts
  
  if total_local_conflicts >= resource.capacity:
    conflict_list.append(Conflict(local_other_conflicts, ValidationError(
      _('Resource at max capacity for requested time slot.'),
      code='invalid')))
 
  return conflict_list
