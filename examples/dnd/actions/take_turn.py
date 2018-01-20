from examples.dnd.actions.character_action import CharacterAction

class TakeTurn(CharacterAction):
  name = 'TakeTurn'

  def execute(self, diff, options):
    for action in self.entity.state.get('planned_actions'):
      action.resolve()

    return {}

  def get_should_react(self, trigger_action, diff, is_preparation):
    return not is_preparation and trigger_action.name is 'StartRound'
