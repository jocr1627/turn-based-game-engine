from engine.deep_merge import deep_merge
from engine.listener import Listener
from examples.dnd.attack_types import AttackTypes

class BluntWeaponFocus(Listener):
  def execute(self, diff):
    trigger = self.get_trigger()
    rank = self.get('rank')
    round_number = self.game.get_round_number()
    requestor = trigger.hydrate('requestor_id')
    target_characters = requestor.get_targets()

    for character in target_characters:
      character.stagger()

      if rank >= 2:
        character.knockdown()

  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      { 'rank': 1 }
    )
  
  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      ['Request']
    )

  def get_should_react(self, diff):
    trigger = self.get_trigger()
    key = trigger.get('key')

    return (
      key is 'is_critical'
      and trigger.get(key) is True
      and trigger.parent is self.parent
      and trigger.get_in(['args', 'attack_type']) is AttackTypes.BLUNT
    )
