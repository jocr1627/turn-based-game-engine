from engine.action import Action
from engine.request import request
from examples.dnd.priorities import Priorities

class PlanTurn(Action):
  def execute(self, diff):
    action_class_name = request(self.parent, 'plan_action_class_name')
    action_class = self.root.entity_classes[action_class_name]
    action = action_class(parent=self.parent)
    action.resolve()
