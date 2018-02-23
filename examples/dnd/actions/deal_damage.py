from engine.action import Action
from examples.dnd.actions.die import Die

class DealDamage(Action):
  def execute(self, diff):
    damage = self.get('damage')
    name = self.parent.get('name')
    hp = self.parent.get('hp')
    hp = hp - damage if hp >= damage else 0
    self.parent.set('hp', hp)
    self.parent.set('has_taken_damage', True)
    print(f'{name} took {damage} points of damage ({hp} points remain).')

    if hp == 0:
      self.parent.die()
