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
      weapon = self.parent.get_weapon()
      damage = 0
      
      for sides,num in weapon.get('dice').items():
        for i in range(num):
          roll = None

          while roll is None:
            raw_roll = input(f'Enter {name}\'s d{sides} roll: ')

            try:
              roll = int(raw_roll)
            except ValueError:
              print(f'{raw_roll} is not a valid roll.')
          
          damage += roll

      damage += sum([modifier for modifier in weapon.get('damage_modifiers').values()])
      deal_damage = DealDamage(parent=target_character, state={ 'damage': damage })
      deal_damage.resolve()
    else:
      print(f'{target_character_name} successfully defended against {name}\'s Attack.')

  def get_default_state(self):
    return { 'attack_modifiers': {}, 'damage_modifiers': {}, 'roll': 0, 'target_character_id': None }

  def get_initiative(self):
    return self.get_score()
  
  def get_is_flanking(self):
    targets_target_character_id = self.hydrate('target_character_id').hydrate('planned_action_id').get('target_character_id')

    return targets_target_character_id is not self.parent.id

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
