from engine.entity import Entity
from examples.dnd.actions.plan_turn import PlanTurn
from examples.dnd.actions.take_turn import TakeTurn

class Character(Entity):
  def get_default_reactions(self, game):
    return [
      PlanTurn,
      TakeTurn,
    ]
  
  def get_default_state(self, game):
    return {
      'actions': {},
      'charisma': 0,
      'initiative': 0,
      'name': None,
      'planned_actions': []
    }
