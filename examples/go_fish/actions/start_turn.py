from engine.deep_merge import deep_merge
from engine.listener import Listener

class StartTurn(Listener):
  def execute(self, diff):
    self.game.set('active_player_id', self.parent.id)

  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      ['StartRound']
    )
