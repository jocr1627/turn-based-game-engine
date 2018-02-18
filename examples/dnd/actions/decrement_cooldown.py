from engine.action import Phases
from engine.base_entity_listener import BaseEntityListener

class DecrementCooldown(BaseEntityListener):
  def execute(self, diff):
    self.parent.update('remaining_cooldown', lambda remaining_cooldown: max(remaining_cooldown - 1, 0))
  
  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      self.parent.get('remaining_cooldown') > 0
      and trigger.is_type('StartRound')
      and trigger.phase is Phases.EXECUTION
    )
