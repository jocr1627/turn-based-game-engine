from engine.action import Phases
from engine.listener import Listener

class EndTurn(Listener):
  def execute(self, diff):
    self.game.set('active_player_id', None)

  def get_is_valid(self, diff):
    return self.parent.id is self.game.get('active_player_id')

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.phase is Phases.EXECUTION
      and trigger.get_name() is 'Request'
      and self.parent.id is self.game.get('active_player_id')
    )
