from engine.deep_merge import deep_merge
from examples.dnd.actions.duration_effect import DurationEffect

class SlashingCriticalEffect(DurationEffect):
  def execute(self, diff):
    trigger = self.get_trigger()
    key = trigger.get('key')
    rank = self.get('rank')
    trigger.update(key, lambda roll: (roll[0], roll[1] - 3 * rank))

  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      ['Request']
    )

  def get_should_react(self, diff):
    trigger = self.get_trigger()
    dice = trigger.get_in(['args', 'dice'])

    return (
      trigger.get('key') is 'roll'
      and trigger.parent is self.parent
      and (dice is None or dice == { 20: 1 })
    )
