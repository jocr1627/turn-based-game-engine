from engine.action import Action
from examples.dnd.actions.rest import Rest

class PlanRest(Action):
  def execute(self, diff):
    rest = Rest(parent=self.parent)
    self.parent.set('planned_action_id', rest.id)
