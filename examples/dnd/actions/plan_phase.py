from engine.action import Phases
from engine.base_entity_listener import BaseEntityListener
from examples.dnd.actions.plan_turn import PlanTurn

class PlanPhase(BaseEntityListener):
  def execute(self, diff):
    characters = self.game.hydrate('character_ids')

    for character in characters:
      plan_turn = PlanTurn(parent=character)
      plan_turn.resolve()

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return trigger.phase is Phases.PREPARATION and trigger.get_name() is 'StartRound'
