from engine.action import Action

class Move(Action):
  def execute(self, diff):
    target_location = self.hydrate('target_location_id')
    target_location.add_child(self.parent)
    name = self.parent.get('name')
    target_location_name = target_location.get('name')
    print(f'{name} moved to {target_location_name}.')
