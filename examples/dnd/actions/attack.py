from engine.action import Action
from engine.normalize_priority import normalize_priority
from engine.request import request
from examples.dnd.priorities import Priorities
from examples.dnd.actions.deal_damage import DealDamage
from examples.dnd.actions.defend import Defend

class Attack(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    target_character = self.hydrate('target_character_id')
    target_character_name = target_character.get('name')
    defend = Defend(parent=target_character, state={ 'attack_id': self.id })
    defend.resolve()
    base_roll = self.get('base_roll')
    attack_score = self.get('score')
    base_defense_roll = defend.get('base_roll')
    defense_score = defend.get('score')

    if base_defense_roll != 20 and base_roll != 1 and (base_roll == 20 or attack_score > defense_score):
      weapon = self.hydrate('weapon_id')
      dice = weapon.get('dice')
      damage_roll_args = { 'action_id': self.id, 'dice': dice, 'roll_type': 'damage' }
      base_damage_roll,modified_damage_roll = request(self, self.parent, 'roll', args=damage_roll_args)
      is_critical_args = args={ 'base_roll': base_roll, 'target_character_ids': [target_character.id] }
      is_critical = request(self, self.parent, 'is_critical', args=is_critical_args)
      critical_factor = request(self, self.parent, 'critical_factor')
      weapon_damage_args = { 'action_id': self.id, 'critical_factor': critical_factor, 'is_critical': is_critical, 'roll': modified_damage_roll, 'weapon_id': weapon.id }
      damage = request(self, self.parent, 'weapon_damage', args=weapon_damage_args)
      deal_damage = DealDamage(parent=target_character, state={ 'damage': damage })
      deal_damage.resolve()
    else:
      print(f'{target_character_name} successfully defended against {name}\'s Attack.')

  def get_default_state(self):
    return { 'base_roll': None, 'modified_roll': None, 'score': None, 'target_character_id': None, 'weapon_id': None }

  def get_initiative(self):
    score = self.get('score')
    initiative = score if score is not None else 0

    return normalize_priority(Priorities.STANDARD_ACTION, initiative)

  def get_is_valid(self, diff):
    return (
      (not self.hydrate('weapon_id').get('is_ranged') or not self.parent.get('has_taken_damage'))
      and self.parent.get('is_alive')
      and self.hydrate('target_character_id').get('is_alive')
    )
