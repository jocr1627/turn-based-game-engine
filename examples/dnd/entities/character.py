from engine.entity import Entity
from examples.dnd.actions.plan_turn import PlanTurn
from examples.dnd.actions.take_turn import TakeTurn

class Character(Entity):
  def __init__(self, name, abilities={}):
    state = { 'abilities': abilities, 'name': name }
    super().__init__(state=state)

  def get_default_children(self):
    return [
      PlanTurn(),
      TakeTurn(),
    ]
  
  def get_default_state(self):
    return {
      'planned_action_id': None
    }
