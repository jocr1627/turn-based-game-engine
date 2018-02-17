from engine.action import Action
from engine.normalize_priority import normalize_priority
from engine.request import request
from examples.dnd.actions.deal_damage import DealDamage
from examples.dnd.actions.defend import Defend
from examples.dnd.entities.attack import Attack
from examples.dnd.entities.base_character import BaseCharacter
from examples.dnd.utils.get_entities_in_range import get_entities_in_range
from examples.dnd.priorities import Priorities

class FinalizeAttack(Action):
  def execute(self, diff):
    modified_roll = self.parent.get_in(['resolve_args', 'modified_roll'])
    target_character_id = self.parent.get_in(['resolve_args', 'target_character_id'])
    weapon_id = self.parent.get_in(['resolve_args', 'weapon_id'])
    weapon_attack_modifier = request(self, self.parent.parent, 'weapon_attack_modifier', args={ 'weapon_id': weapon_id })
    is_flanking = request(self, self.parent.parent, 'is_flanking', args={ 'target_character_id': target_character_id })
    score = modified_roll + weapon_attack_modifier

    if is_flanking:
      score += 2

    self.parent.set_in(['resolve_args', 'score'], score)

class PrepareAttack(Action):
  def execute(self, diff):
    max_range = -1 if self.parent.parent.get_weapon().get('is_ranged') else 0
    valid_target_character_ids = get_entities_in_range(self.parent.parent.parent, max_range, self.parent.other_character_filter)
    target_character_id_args = { 'action_id': self.parent.id, 'num_targets': 1, 'valid_ids': valid_target_character_ids }
    target_character_ids = request(self, self.parent.parent, 'target_character_ids', args=target_character_id_args)
    target_character_id = target_character_ids[0] if len(target_character_ids) > 0 else None
    base_roll, modified_roll = request(self, self.parent.parent, 'roll', args={ 'action_id': self.parent.id, 'roll_type': 'attack' })
    weapon = self.parent.parent.get_weapon()
    resolve_args = { 'base_roll': base_roll, 'modified_roll': modified_roll, 'target_character_id': target_character_id, 'weapon_id': weapon.id }
    self.parent.set('resolve_args', resolve_args)

class ResolveAttack(Action):
  def execute(self, diff):
    name = self.parent.parent.get('name')
    target_character = self.hydrate_in(['resolve_args', 'target_character_id'])
    target_character_name = target_character.get('name')
    defend = Defend(parent=target_character, state={ 'attack_id': self.id })
    defend.resolve()
    base_roll = self.get_in(['resolve_args', 'base_roll'])
    attack_score = self.get_in(['resolve_args', 'score'])
    base_defense_roll = defend.get('base_roll')
    defense_score = defend.get('score')

    if base_defense_roll != 20 and base_roll != 1 and (base_roll == 20 or attack_score > defense_score):
      weapon = self.hydrate_in(['resolve_args', 'weapon_id'])
      dice = weapon.get('dice')
      damage_roll_args = { 'action_id': self.id, 'dice': dice, 'roll_type': 'damage' }
      base_damage_roll,modified_damage_roll = request(self, self.parent.parent, 'roll', args=damage_roll_args)
      is_critical_args = args={ 'base_roll': base_roll, 'target_character_ids': [target_character.id] }
      is_critical = request(self, self.parent.parent, 'is_critical', args=is_critical_args)
      critical_factor = request(self, self.parent.parent, 'critical_factor')
      weapon_damage_args = { 'action_id': self.id, 'critical_factor': critical_factor, 'is_critical': is_critical, 'roll': modified_damage_roll, 'weapon_id': weapon.id }
      damage = request(self, self.parent.parent, 'weapon_damage', args=weapon_damage_args)
      deal_damage = DealDamage(parent=target_character, state={ 'damage': damage })
      deal_damage.resolve()
    else:
      print(f'{target_character_name} successfully defended against {name}\'s Attack.')

  def get_is_valid(self, diff):
    return (
      (not self.hydrate_in(['resolve_args', 'weapon_id']).get('is_ranged') or not self.parent.parent.get('has_taken_damage'))
      and self.parent.parent.get('is_alive')
      and self.hydrate_in(['resolve_args', 'target_character_id']).get('is_alive')
    )

class Cleave(Attack):
  matcher = r'cleave'

  def finalize(self):
    finalize_attack = FinalizeAttack(parent=self)
    finalize_attack.resolve()

  def get_is_possible(self):
    is_ranged = self.parent.get_weapon().get('is_ranged')

    return not is_ranged and len(get_entities_in_range(self.parent.parent, 0, self.other_character_filter)) >= 2

  def prepare(self):
    prepare_attack = PrepareAttack(parent=self)
    prepare_attack.resolve()

  def resolve(self):
    resolve_attack = ResolveAttack(parent=self, state={ 'resolve_args': self.get('resolve_args') })
    resolve_attack.resolve()
