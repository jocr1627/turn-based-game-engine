from engine.action import Action

class StartTurn(Action):
  name = 'StartTurn'

  def execute(self):
    active_player = self.game.state['active_player']
    self.game.state['active_player'] = self.entity

    return { self.game.id: { 'active_player': (active_player, self.entity) } }

  def get_is_valid(self):
    return self.entity.does_exist

  def get_should_react(self, trigger_action, is_preparation):
    return not is_preparation and trigger_action.name is 'StartRound'
