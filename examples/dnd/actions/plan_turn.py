from engine.action import Action
from engine.request import request
from examples.dnd.actions.plan_advance import PlanAdvance
from examples.dnd.actions.plan_attack import PlanAttack
from examples.dnd.actions.plan_equip import PlanEquip
from examples.dnd.actions.plan_flee import PlanFlee
from examples.dnd.actions.plan_move import PlanMove
from examples.dnd.priorities import Priorities

plan_classes = [
  PlanAdvance,
  PlanAttack,
  PlanEquip,
  PlanFlee,
  PlanMove
]
plan_class_map = { clazz.get_name(): clazz for clazz in plan_classes }

class PlanTurn(Action):
  def execute(self, diff):
    action_class_name = request(self, self.parent, 'plan_action_class_name')

    if action_class_name is not None:
      abilities = self.parent.get('abilities')
      action_class = plan_class_map[action_class_name]
      action_config = abilities[action_class_name]
      action = action_class(parent=self.parent, **action_config)
      action.resolve()
