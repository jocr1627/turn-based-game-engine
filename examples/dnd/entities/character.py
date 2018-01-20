from engine.entity import Entity
from examples.dnd.actions.plan_turn import PlanTurn
from examples.dnd.actions.take_turn import TakeTurn

class Character(Entity):
  def get_default_children(self):
    return [
      PlanTurn(),
      TakeTurn(),
    ]
  
  def get_default_state(self):
    return {
      'abilities': {},
      'name': None,
      'planned_action_id': None
    }
