import re
from engine.action import Action

class Equip(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    weapon = self.hydrate('weapon_id')
    weapon_id = weapon.id if weapon is not None else None
    weapon_name = weapon.get('name') if weapon is not None else 'nothing'
    self.parent.set('weapon_id', weapon_id)
    print(f'{name} equipped {weapon_name}.')

  def get_initiative(self):
    return -1