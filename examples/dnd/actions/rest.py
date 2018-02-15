from engine.action import Action
from examples.dnd.priorities import Priorities

class Rest(Action):
  def execute(self, diff):
    max_mp = self.parent.get('max_mp')
    self.parent.set('mp', max_mp)

  def get_initiative(self):
    return Priorities.NO_ROLL_ACTION

  def get_is_valid(self, diff):
    return self.parent.get('is_alive')
