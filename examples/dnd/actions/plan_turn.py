import re
from engine.listener import Listener
from engine.request import request

class PlanTurn(Listener):
  def execute(self, diff):
    action_class_name = request(self.parent, 'plan_action_class_name')
    action_class = self.root.entity_classes[action_class_name]
    action = action_class(parent=self.parent)
    action.resolve()

  def get_should_react(self, trigger_action, diff, is_preparation):
    return is_preparation and trigger_action.get_name() is 'StartRound'
