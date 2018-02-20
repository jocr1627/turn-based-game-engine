from engine.deep_merge import deep_merge
from engine.listener import Listener

class ClearInterrupt(Listener):
  def execute(self, diff):
    self.parent.set('has_taken_damage', False)

  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      ['EndRound']
    )
