from engine.action import Action

class StartTurn(Action):
  name = 'StartTurn'

  def execute(self):
    return self.game.state.set('active_player', self.entity.id)

  def get_is_valid(self):
    return self.entity.does_exist

  def get_should_react(self, trigger_action, is_preparation):
    return not is_preparation and trigger_action.name is 'StartRound'
