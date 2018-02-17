from engine.action import Phases
from engine.base_entity_listener import BaseEntityListener

class EnforceRest(BaseEntityListener):
  def execute(self, diff):
    trigger = self.get_trigger()
    key = trigger.get('key')
    rest_id = self.parent.get_in(['abilities', 'Rest'])
    trigger.set(key, rest_id)

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.phase is Phases.EXECUTION
      and trigger.get_name() is 'Request'
      and trigger.get('key') is 'ability_id'
      and trigger.parent is self.parent
      and self.parent.get('mp') == 0
    )
