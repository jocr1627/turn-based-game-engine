from engine.deep_merge import deep_merge
from engine.listener import Listener

class PiercingCriticalEffect(Listener):
  is_self_destructive = True

  def execute(self, diff):
    trigger = self.get_trigger()
    key = trigger.get('key')
    rank = self.get('rank')
    trigger.set(key, 2 + 0.5 * rank)

  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      ['Request']
    )

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.get('key') is 'critical_factor'
      and trigger.parent is self.parent
    )
