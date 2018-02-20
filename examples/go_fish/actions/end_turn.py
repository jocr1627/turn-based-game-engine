from engine.deep_merge import deep_merge
from engine.listener import Listener

class EndTurn(Listener):
  def execute(self, diff):
    self.game.set('active_player_id', None)

  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      ['Request']
    )

  def get_is_valid(self, diff):
    return self.parent.id is self.game.get('active_player_id')

  def get_should_react(self, diff):
    return self.parent.id is self.game.get('active_player_id')
