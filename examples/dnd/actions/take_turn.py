from engine.action import Action
from examples.dnd.actions.character_action import CharacterAction

class TakeTurn(CharacterAction):
  name = 'TakeTurn'

  def execute(self):
    for action in self.entity.state['planned_actions']:
      action.resolve()

    return {}

  def get_should_react(self, trigger_action, is_preparation):
    return not is_preparation and trigger_action.name is 'StartRound'
