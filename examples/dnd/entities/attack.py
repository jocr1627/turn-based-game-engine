from engine.action import Action
from engine.normalize_priority import normalize_priority
from engine.request import request
from examples.dnd.actions.deal_damage import DealDamage
from examples.dnd.actions.defend import Defend
from examples.dnd.entities.ability import Ability
from examples.dnd.entities.base_character import BaseCharacter
from examples.dnd.utils.get_entities_in_range import get_entities_in_range
from examples.dnd.priorities import Priorities

class FinalizeAttack(Action):
  def execute(self, diff):
    modified_roll = self.parent.get('modified_roll')
    target_character_id = self.parent.get('target_character_id')
    weapon_id = self.parent.get('weapon_id')
    weapon_attack_modifier = request(self, self.parent.parent, 'weapon_attack_modifier', args={ 'weapon_id': weapon_id })
    is_flanking = request(self, self.parent.parent, 'is_flanking', args={ 'target_character_id': target_character_id })
    score = modified_roll + weapon_attack_modifier

    if is_flanking:
      score += 2

    self.parent.set('score', score)

class PrepareAttack(Action):
  def execute(self, diff):
    num_targets = self.parent.get('num_targets')
    weapon = self.parent.parent.get_weapon()
    max_range = -1 if weapon.get('is_ranged') else 0
    valid_target_character_ids = get_entities_in_range(self.parent.parent.parent, max_range, self.parent.other_character_filter)
    target_character_id_args = { 'action_id': self.parent.id, 'num_targets': num_targets, 'valid_ids': valid_target_character_ids }
    target_character_ids = request(self, self.parent.parent, 'target_character_ids', args=target_character_id_args)
    target_character_id = target_character_ids[0] if len(target_character_ids) > 0 else None
    base_roll, modified_roll = request(self, self.parent.parent, 'roll', args={ 'action_id': self.parent.id, 'roll_type': 'attack' })
    self.parent.set('base_roll', base_roll)
    self.parent.set('modified_roll', modified_roll)
    self.parent.set('target_character_id', target_character_id)
    self.parent.set('weapon_id', weapon.id)

class ResolveAttack(Action):
  def execute(self, diff):
    name = self.get_ability().parent.get('name')
    target_character = self.parent.hydrate('target_character_id')
    target_character_name = target_character.get('name')
    defend = Defend(parent=target_character, state={ 'attack_id': self.id })
    defend.resolve()
    base_roll = self.parent.get('base_roll')
    attack_score = self.parent.get('score')
    base_defense_roll = defend.get('base_roll')
    defense_score = defend.get('score')

    if base_defense_roll != 20 and base_roll != 1 and (base_roll == 20 or attack_score > defense_score):
      weapon = self.parent.hydrate('weapon_id')
      dice = weapon.get('dice')
      damage_roll_args = { 'action_id': self.parent.id, 'dice': dice, 'roll_type': 'damage' }
      base_damage_roll,modified_damage_roll = request(self, self.parent.parent, 'roll', args=damage_roll_args)
      attack_type = weapon.get('attack_type')
      is_critical_args = args={ 'attack_type': attack_type, 'base_roll': base_roll, 'target_character_ids': [target_character.id] }
      is_critical = request(self, self.parent.parent, 'is_critical', args=is_critical_args)
      critical_factor = request(self, self.parent.parent, 'critical_factor')
      weapon_damage_args = { 'action_id': self.parent.id, 'critical_factor': critical_factor, 'is_critical': is_critical, 'roll': modified_damage_roll, 'weapon_id': weapon.id }
      damage = request(self, self.parent.parent, 'weapon_damage', args=weapon_damage_args)
      deal_damage = DealDamage(parent=target_character, state={ 'damage': damage })
      deal_damage.resolve()
    else:
      print(f'{target_character_name} successfully defended against {name}\'s Attack.')

  def get_is_valid(self, diff):
    return (
      (not self.parent.hydrate('weapon_id').get('is_ranged') or not self.parent.parent.get('has_taken_damage'))
      and self.parent.parent.get('is_alive')
      and self.parent.hydrate('target_character_id').get('is_alive')
    )

class Attack(Ability):
  matcher = r'attack'

  def finalize(self):
    finalize_attack = FinalizeAttack(parent=self)
    finalize_attack.resolve()
  
  def get_default_state(self):
    return {
      'base_roll': None,
      'modified_roll': None,
      'num_targets': 1,
      'score': None,
      'target_character_id': None
    }

  def get_initiative(self):
    score = self.get('score')
    initiative = score if score is not None else 0

    return normalize_priority(Priorities.STANDARD_ACTION, initiative)

  def get_is_possible(self):
    max_range = -1 if self.parent.get_weapon().get('is_ranged') else 0

    return len(get_entities_in_range(self.parent.parent, max_range, self.other_character_filter)) > 0

  def other_character_filter(self, entity):
    return isinstance(entity, BaseCharacter) and not entity is self.parent

  def prepare(self):
    prepare_attack = PrepareAttack(parent=self)
    prepare_attack.resolve()

  def resolve(self):
    resolve_attack = ResolveAttack(parent=self)
    resolve_attack.resolve()
