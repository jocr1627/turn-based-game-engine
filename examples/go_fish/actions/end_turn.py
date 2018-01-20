from engine.listener import Listener

class EndTurn(Listener):
  def execute(self, diff):
    self.root.set('active_player_id', None)

  def get_is_valid(self):
    return self.parent.id is self.root.get('active_player_id')

  def get_should_react(self, trigger_action, diff, is_preparation):
    return (
      not is_preparation
      and trigger_action.get_name() is 'Request'
      and self.parent.id is self.root.get('active_player_id')
    )
