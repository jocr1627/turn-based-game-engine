from engine.action import Action
from examples.dnd.actions.character_action import CharacterAction
from examples.dnd.actions.whistle import Whistle
from examples.dnd.actions.choose_character_target import ChooseCharacterTarget

class PlanWhistle(CharacterAction):
  name = 'PlanWhistle'

  def execute(self):
    whistle_action = Whistle(self.game, self.entity)
    ChooseCharacterTarget(self.game, self.entity, { 'action': whistle_action }).resolve()
    planned_actions = self.entity.state['planned_actions']
    new_planned_actions = [whistle_action]
    self.entity.state['planned_actions'] = new_planned_actions

    return { self.entity.id: { 'planned_actions': (planned_actions, new_planned_actions) } }
