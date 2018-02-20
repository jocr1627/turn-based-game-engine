from engine.deep_merge import deep_merge
from engine.listener import Listener

class DecrementCooldown(Listener):
  def execute(self, diff):
    self.parent.update('remaining_cooldown', lambda remaining_cooldown: max(remaining_cooldown - 1, 0))
  
  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      ['StartRound']
    )

  def get_should_react(self, diff):
    return self.parent.get('remaining_cooldown') > 0
