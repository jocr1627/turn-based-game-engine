from engine.action import Action
from examples.dnd.actions.character_action import CharacterAction
from examples.dnd.actions.impotent_rage import ImpotentRage

class PlanImpotentRage(CharacterAction):
  name = 'PlanImpotentRage'

  def execute(self):
    planned_actions = self.entity.state['planned_actions']
    new_planned_actions = [ImpotentRage(self.game, self.entity)]
    self.entity.state['planned_actions'] = new_planned_actions

    return { self.entity.id: { 'planned_actions': (planned_actions, new_planned_actions) } }
