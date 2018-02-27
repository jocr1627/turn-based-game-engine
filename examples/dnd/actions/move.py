from engine.action import Action

class Move(Action):
  def execute(self, diff):
    location = self.hydrate('location_id')
    location.add_child(self.parent)

  def get_is_valid(self, diff):
    return self.parent.get('is_alive')
