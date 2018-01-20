from engine.listener import Listener

class EndTurn(Listener):
  name = 'EndTurn'

  def execute(self, diff, options):
    self.root.set('active_player_id', None)

  def get_is_valid(self, options):
    return self.parent.id is self.root.get('active_player_id')

  def get_should_react(self, trigger_action, diff, is_preparation):
    return (
      not is_preparation
      and trigger_action.name is 'Request'
      and self.parent.id is self.root.get('active_player_id')
    )
