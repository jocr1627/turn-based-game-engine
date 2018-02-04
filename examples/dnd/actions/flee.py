import re
from engine.action import Action

class Flee(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    current_location = self.parent.parent
    flee_location = self.hydrate('target_location_id')
    flee_location_name = flee_location.get('name')
    target = self.hydrate('target_id')
    target_name = target.get('name')
    target_location = target.parent

    if target_location is flee_location:
      flee_location = current_location

    if flee_location is not current_location:
      flee_location.add_child(self.parent)
      print(f'{name} fleed from {target_name} to {flee_location_name}.')
    else:
      print(f'{name} stayed put.')

  def get_initiative(self):
    return -3
