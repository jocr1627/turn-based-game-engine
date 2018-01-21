from engine.listener import Listener

class StartTurn(Listener):
  def execute(self, diff):
    self.root.set('active_player_id', self.parent.id)

  def get_should_react(self, trigger_action, diff, is_preparation):
    return not is_preparation and trigger_action.get_name() is 'StartRound'
