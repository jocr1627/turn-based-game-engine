from engine.action import Action

class Die(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    self.parent.set('is_alive', False)
    print(f'{name} has died!')
