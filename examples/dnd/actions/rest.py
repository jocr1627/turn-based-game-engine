from engine.action import Action
from examples.dnd.priorities import Priorities

class Rest(Action):
  def execute(self, diff):
    max_mp = self.parent.get('max_mp')
    self.parent.set('mp', max_mp)

  def get_priority(self):
    return Priorities.NO_ROLL_ACTION
