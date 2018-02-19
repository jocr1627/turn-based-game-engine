from engine.action import Phases
from engine.deep_merge import deep_merge
from engine.listener import Listener

class EnforceRest(Listener):
  def execute(self, diff):
    trigger = self.get_trigger()
    key = trigger.get('key')
    rest_id = self.parent.get_in(['abilities', 'Rest'])
    trigger.set(key, rest_id)

  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      [('Request', Phases.EXECUTION)]
    )

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.get('key') is 'ability_id'
      and trigger.parent is self.parent
      and self.parent.get('mp') == 0
    )
