from engine.action import Phases
from examples.dnd.actions.duration_effect import DurationEffect

class SlashingCriticalEffect(DurationEffect):
  def execute(self, diff):
    trigger = self.get_trigger()
    key = trigger.get('key')
    trigger.update(key, lambda roll: (roll[0], roll[1] - 3))

  def get_should_react(self, diff):
    trigger = self.get_trigger()
    dice = trigger.get_in(['args', 'dice'])

    return (
      trigger.phase is Phases.EXECUTION
      and trigger.get_name() is 'Request'
      and trigger.get('key') is 'roll'
      and trigger.parent is self.parent
      and (dice is None or dice == { 20: 1 })
    )
