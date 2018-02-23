from engine.deep_merge import deep_merge
from engine.listener import Listener
from examples.dnd.attack_types import AttackTypes
from examples.dnd.actions.slashing_critical_effect import SlashingCriticalEffect

class SlashingWeaponFocus(Listener):
  def execute(self, diff):
    trigger = self.get_trigger()
    rank = self.get('rank')
    round_number = self.game.get('round_number')
    requestor = trigger.hydrate('requestor_id')
    target_characters = requestor.get_targets()

    for character in target_characters:
      SlashingCriticalEffect(parent=character, state={ 'rank': rank, 'starting_round_number': round_number })

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
    requestor = trigger.hydrate('requestor_id')

    return (
      key is 'is_critical'
      and trigger.get(key) is True
      and trigger.parent is self.parent
      and trigger.get_in(['args', 'attack_type']) is AttackTypes.SLASHING
    )
