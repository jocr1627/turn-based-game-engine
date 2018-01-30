import re
from engine.action import Action
from examples.dnd.priorities import Priorities

class Advance(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    current_location = self.parent.parent
    original_target_location = self.hydrate('original_target_location_id')
    target_character = self.hydrate('target_character_id')
    target_character_name = target_character.get('name')
    target_location = target_character.parent
    neighbors = current_location.hydrate('neighbor_ids')
    possible_locations = [current_location] + neighbors
    advance_location = target_location if target_location in possible_locations else original_target_location
    advance_location_name = advance_location.get('name')

    if advance_location is not current_location:
      advance_location.add_child(self.parent)
      print(f'{name} advanced on {target_character_name} to {advance_location_name}.')
    else:
      print(f'{name} stayed put.')

  def get_priority(self):
    return Priorities.ADVANCE
