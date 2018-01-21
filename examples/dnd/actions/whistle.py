from engine.action import Action

class Whistle(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    target = self.hydrate('target_id')
    target_name = target.get('name')
    print(f'{name} whistled to {target_name}')
