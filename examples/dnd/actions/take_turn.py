from examples.dnd.actions.character_action import CharacterAction

class TakeTurn(CharacterAction):
  def execute(self, diff):
    for action in self.entity.state.get('planned_actions'):
      action.resolve()

    return {}

  def get_should_react(self, trigger_action, diff, is_preparation):
    return not is_preparation and trigger_action.get_name() is 'StartRound'
