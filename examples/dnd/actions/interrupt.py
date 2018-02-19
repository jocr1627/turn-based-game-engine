from engine.deep_merge import deep_merge
from engine.listener import Listener

class Interrupt(Listener):
  def execute(self, diff):
    self.parent.set('has_taken_damage', True)

  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      [None]
    )

  def get_should_react(self, diff):
    hp_diff = diff.get_in(['state', self.parent.id, 'hp'])

    return (
      hp_diff is not None
      and hp_diff[1] < hp_diff[0]
    )
