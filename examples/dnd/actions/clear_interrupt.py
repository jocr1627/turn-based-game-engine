from engine.action import Phases
from engine.base_entity_listener import BaseEntityListener

class ClearInterrupt(BaseEntityListener):
  def execute(self, diff):
    self.parent.set('has_taken_damage', False)

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.phase is Phases.EXECUTION
      and trigger.get_name() is 'EndRound'
    )
