from engine.action import Phases
from engine.listener import Listener

class SetTargetCharacter(Listener):
  def execute(self, diff):
    trigger = self.get_trigger()
    target_character_ids = trigger.get('target_character_ids')
    target_character_id = None

    if isinstance(target_character_ids, list) and len(target_character_ids) == 1:
      target_character_id = target_character_ids[0]

    self.parent.set('target_character_id', target_character_id)

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.phase is Phases.EXECUTION
      and trigger.get_name() is 'Request'
      and trigger.get('key') is 'target_character_ids'
      and trigger.parent is self.parent
    )