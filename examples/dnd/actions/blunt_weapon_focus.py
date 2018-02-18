from engine.action import Phases
from engine.base_entity_listener import BaseEntityListener
from engine.deep_merge import deep_merge
from examples.dnd.attack_types import AttackTypes

class BluntWeaponFocus(BaseEntityListener):
  def execute(self, diff):
    trigger = self.get_trigger()
    rank = self.get('rank')
    round_number = self.game.get('round_number')
    target_characters = trigger.hydrate_in(['args', 'target_character_ids'])

    for character in target_characters:
      character.set('staggered', True)
        
      if rank >= 2:
        character.set('prone', True)

  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      { 'rank': 1 }
    )

  def get_should_react(self, diff):
    trigger = self.get_trigger()
    key = trigger.get('key')
    requestor = trigger.hydrate('requestor_id')

    return (
      trigger.phase is Phases.EXECUTION
      and trigger.get_name() is 'Request'
      and key is 'is_critical'
      and trigger.get(key) is True
      and trigger.parent is self.parent
      and trigger.get_in(['args', 'attack_type']) is AttackTypes.BLUNT
    )
