import re
from engine.action import Action
from examples.dnd.priorities import Priorities

class Flee(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    current_location = self.parent.parent
    flee_location = self.hydrate('target_location_id')
    flee_location_name = flee_location.get('name')
    target_character = self.hydrate('target_character_id')
    target_character_name = target_character.get('name')
    target_location = target_character.parent

    if target_location is flee_location:
      flee_location = current_location

    if flee_location is not current_location:
      flee_location.add_child(self.parent)
      print(f'{name} fleed from {target_character_name} to {flee_location_name}.')
    else:
      print(f'{name} stayed put.')
    
  def get_is_valid(self):
    return self.hydrate('target_location_id') is not None

  def get_priority(self):
    return Priorities.FLEE
