from engine.action import Phases
from engine.listener import Listener
from examples.dnd.attack_types import AttackTypes
from examples.dnd.actions.slashing_critical_effect import SlashingCriticalEffect

attack_types_to_effects = {
  AttackTypes.SLASHING: SlashingCriticalEffect
}

class WeaponFocus(Listener):
  def execute(self, diff):
    trigger = self.get_trigger()
    requestor = trigger.hydrate('requestor_id')
    attack_type = requestor.parent.get_weapon().get('attack_type')
    EffectClass = attack_types_to_effects[attack_type] if attack_type in attack_types_to_effects else None

    if EffectClass is not None:
      round_number = self.root.get('round_number')
      target_characters = trigger.hydrate_in(['args', 'target_character_ids'])

      for character in target_characters:
        EffectClass(parent=character, state={ 'starting_round_number': round_number })

  def get_should_react(self, diff):
    trigger = self.get_trigger()
    key = trigger.get('key')

    return (
      trigger.phase is Phases.EXECUTION
      and trigger.get_name() is 'Request'
      and key is 'is_critical'
      and trigger.get(key) is True
      and trigger.parent is self.parent
    )
