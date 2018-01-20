from engine.action import Action

class Whistle(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    target_id = self.get('target_id')
    target = self.root.descendants[target_id]
    target_name = target.get('name')
    print(f'{name} whistled to {target_name}')
