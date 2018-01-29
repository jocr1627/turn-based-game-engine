from engine.action import Action
from examples.dnd.actions.deal_damage import DealDamage
from examples.dnd.actions.defend import Defend

class Attack(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    target_character = self.hydrate('target_character_id')
    target_character_name = target_character.get('name')
    defend = Defend(parent=target_character, state={ 'attack_id': self.id })
    defend.resolve()
    roll = self.get('roll')
    attack_score = self.get_score()
    defense_roll = defend.get('roll')
    defense_score = defend.get_score()

    if defense_roll != 20 and roll != 1 and (roll == 20 or attack_score > defense_score):
      is_critical = self.parent.request('is_critical', args={ 'roll': roll })
      damage = self.parent.request('weapon_damage', args={ 'action_id': self.id, 'is_critical': is_critical })
      deal_damage = DealDamage(parent=target_character, state={ 'damage': damage })
      deal_damage.resolve()
    else:
      print(f'{target_character_name} successfully defended against {name}\'s Attack.')

  def get_default_state(self):
    return { 'attack_modifiers': {}, 'damage_modifiers': {}, 'roll': 0, 'target_character_id': None }

  def get_initiative(self):
    return self.get_score()
  
  def get_is_flanking(self):
    target_character_id = self.get('target_character_id')

    return self.parent.request('is_flanking', args={ 'target_character_id': target_character_id })

  def get_score(self):
    score = self.get('roll')
    score += sum([modifier for modifier in self.get('attack_modifiers').values()])
    weapon = self.parent.get_weapon()
    weapon_attribute_caps = weapon.get('attribute_caps')
    attributes = self.parent.get('attributes')

    for attribute,cap in weapon_attribute_caps.items():
      attribute_score = attributes[attribute]
      score += min(attribute_score, cap) if cap is not None else attribute_score
    
    score += sum([modifier for modifier in weapon.get('attack_modifiers').values()])

    if self.get_is_flanking():
      score += 2

    return score
