from engine.action import Action

class EndTurn(Action):
  name = 'EndTurn'

  def execute(self):
    return self.game.state.set('active_player', None)

  def get_is_valid(self):
    return self.entity.id is self.game.state.get('active_player')

  def get_should_react(self, trigger_action, is_preparation):
    return (
      not is_preparation
      and trigger_action.name is 'Request'
      and self.entity.id is self.game.state.get('active_player')
    )
