from engine.action import Action, Phases
from examples.dnd.actions.plan_turn import PlanTurn

class PlanPhase(Action):
  def execute(self, diff):
    characters = self.game.hydrate('character_ids')

    for character in characters:
      plan_turn = PlanTurn(parent=character)
      plan_turn.resolve()
