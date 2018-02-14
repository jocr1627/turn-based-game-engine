from engine.action import Phases
from engine.listener import Listener

class PiercingCriticalEffect(Listener):
  def execute(self, diff):
    trigger = self.get_trigger()
    key = trigger.get('key')
    rank = self.get('rank')
    trigger.set(key, 2 + 0.5 * rank)

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.phase is Phases.EXECUTION
      and trigger.get_name() is 'Request'
      and trigger.get('key') is 'critical_factor'
      and trigger.parent is self.parent
    )

  def get_should_terminate(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.phase is Phases.EXECUTION
      and trigger is self.hydrate('attack_id')
    )
