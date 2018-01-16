from engine.action import Action

class EndTurn(Action):
  name = 'EndTurn'

  def execute(self):
    active_player = self.game.state['active_player']
    self.game.state['active_player'] = None

    return { self.game.id: { 'active_player': (active_player, None) } }

  def get_is_valid(self):
    return self.entity is self.game.state['active_player']

  def get_should_react(self, trigger_action, is_preparation):
    return (
      not is_preparation
      and trigger_action.name is 'Request'
      and self.entity is self.game.state['active_player']
    )
