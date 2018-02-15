from engine.action import Action

class DealDamage(Action):
  def execute(self, diff):
    damage = self.get('damage')
    name = self.parent.get('name')
    hp = self.parent.get('hp')
    hp = hp - damage if hp >= damage else 0
    self.parent.set('hp', hp)
    print(f'{name} took {damage} points of damage ({hp} points remain).')

    if hp == 0:
      self.parent.set('is_alive', False)
      print(f'{name} has died!')
