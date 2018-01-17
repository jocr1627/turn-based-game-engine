from engine.action import Action
from examples.dnd.actions.character_action import CharacterAction
from examples.dnd.actions.impotent_rage import ImpotentRage

class PlanImpotentRage(CharacterAction):
  name = 'PlanImpotentRage'

  def execute(self):
    return self.entity.state.set('planned_actions', [ImpotentRage(self.game, self.entity)])
