from engine.action import Phases
from engine.listener import Listener

class DestroyAction(DestroyEntity):
  def get_should_react(self, diff):
    return self.get_trigger() is self.parent

class PiercingCriticalEffect(Listener):
  def execute(self, diff):
    trigger = self.get_trigger()
    key = trigger.get('key')
    rank = self.get('rank')
    trigger.set(key, 2 + 0.5 * rank)

  def get_default_children(self):
    return deep_merge(
      super().get_default_children(),
      [DestroyAction(trigger_types=[(self.get_name(), Phases.EXECUTION)])]
    )

  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      [('Request', Phases.EXECUTION)]
    )

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.get('key') is 'critical_factor'
      and trigger.parent is self.parent
    )
