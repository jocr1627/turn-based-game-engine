from engine.deep_merge import deep_merge
from engine.normalize_priority import normalize_priority
from engine.request import request
from examples.dnd.actions.deal_damage import DealDamage
from examples.dnd.actions.defend import Defend
from examples.dnd.entities.ability import AbilityAction
from examples.dnd.entities.targeted_ability import TargetedAbility
from examples.dnd.utils.get_entities_in_range import get_entities_in_range
from examples.dnd.priorities import Priorities

class FinalizeAttack(AbilityAction):
  def execute(self, diff):
    modified_roll = self.ability.get('modified_roll')
    target_character_id = self.ability.get('target_character_id')
    weapon_id = self.ability.get('weapon_id')
    character = self.ability.character
    weapon_attack_modifier = request(self, character, 'weapon_attack_modifier', args={ 'weapon_id': weapon_id })
    is_flanking = request(self, character, 'is_flanking', args={ 'target_character_id': target_character_id })
    score = modified_roll + weapon_attack_modifier

    if is_flanking:
      score += 2

    self.ability.set('score', score)

class PrepareAttack(AbilityAction):
  def execute(self, diff):
    num_targets = request(self, self.ability, 'num_targets')
    character = self.ability.character
    weapon = character.get_weapon()
    max_range = -1 if weapon.get('is_ranged') else 0
    valid_target_character_ids = self.ability.get_valid_target_ids()
    target_character_id_args = { 'action_id': self.ability.id, 'num_targets': num_targets, 'valid_ids': valid_target_character_ids }
    target_character_ids = request(self, character, 'target_character_ids', args=target_character_id_args)
    target_character_id = target_character_ids[0] if len(target_character_ids) > 0 else None
    base_roll, modified_roll = request(self, character, 'roll', args={ 'action_id': self.ability.id, 'roll_type': 'attack' })
    self.ability.set('base_roll', base_roll)
    self.ability.set('modified_roll', modified_roll)
    self.ability.set('target_character_id', target_character_id)
    self.ability.set('weapon_id', weapon.id)

class ResolveAttack(AbilityAction):
  def execute(self, diff):
    character = self.ability.character
    name = character.get('name')
    target_character = self.ability.hydrate('target_character_id')
    target_character_name = target_character.get('name')
    defend = Defend(parent=target_character, state={ 'attack_id': self.id })
    defend.resolve()
    base_roll = self.ability.get('base_roll')
    attack_score = self.ability.get('score')
    base_defense_roll = defend.get('base_roll')
    defense_score = defend.get('score')

    if base_defense_roll != 20 and base_roll != 1 and (base_roll == 20 or attack_score > defense_score):
      weapon = self.ability.hydrate('weapon_id')
      dice = weapon.get('dice')
      damage_roll_args = { 'action_id': self.ability.id, 'dice': dice, 'roll_type': 'damage' }
      base_damage_roll,modified_damage_roll = request(self, character, 'roll', args=damage_roll_args)
      attack_type = weapon.get('attack_type')
      is_critical_args = args={ 'attack_type': attack_type, 'base_roll': base_roll, 'target_character_ids': [target_character.id] }
      is_critical = request(self, character, 'is_critical', args=is_critical_args)
      critical_factor = request(self, character, 'critical_factor')
      weapon_damage_args = { 'action_id': self.ability.id, 'critical_factor': critical_factor, 'is_critical': is_critical, 'roll': modified_damage_roll, 'weapon_id': weapon.id }
      damage = request(self, character, 'weapon_damage', args=weapon_damage_args)
      deal_damage = DealDamage(parent=target_character, state={ 'damage': damage })
      deal_damage.resolve()
    else:
      print(f'{target_character_name} successfully defended against {name}\'s Attack.')

  def get_is_valid(self, diff):
    character = self.ability.character

    return (
      (not self.ability.hydrate('weapon_id').get('is_ranged') or not character.get('has_taken_damage'))
      and character.get('is_alive')
      and self.ability.hydrate('target_character_id').get('is_alive')
    )

class Attack(TargetedAbility):
  matcher = r'^attack$'

  def finalize(self):
    finalize_attack = FinalizeAttack(parent=self)
    finalize_attack.resolve()
  
  def get_default_getters(self):
    return deep_merge(
      super().get_default_getters(),
      { 'num_targets': self.get_num_targets }
    )
  
  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      {
        'base_roll': None,
        'modified_roll': None,
        'score': None,
        'target_character_id': None
      }
    )

  def get_initiative(self):
    score = self.get('score')
    initiative = score if score is not None else 0

    return normalize_priority(Priorities.STANDARD_ACTION, initiative)

  def get_num_targets(self):
    return 1

  def get_valid_target_ids(self):
    max_range = -1 if self.character.get_weapon().get('is_ranged') else 0

    return get_entities_in_range(self.character.location, max_range, self.other_character_filter)

  def other_character_filter(self, entity):
    return entity.is_type('Character') and not entity is self.character and entity.get('is_alive')

  def prepare(self):
    prepare_attack = PrepareAttack(parent=self)
    prepare_attack.resolve()

  def resolve(self):
    resolve_attack = ResolveAttack(parent=self)
    resolve_attack.resolve()
