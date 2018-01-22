from engine.action import Action
from examples.dnd.actions.deal_damage import DealDamage
from examples.dnd.actions.defend import Defend

class Attack(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    target = self.hydrate('target_id')
    target_name = target.get('name')
    defend = Defend(parent=target, state={ 'attack_id': self.id })
    defend.resolve()
    attack_score = self.get_score()
    defense_score = defend.get_score()

    if attack_score > defense_score:
      weapon = self.parent.hydrate('weapon_id')
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
      deal_damage = DealDamage(parent=target, state={ 'damage': damage })
      deal_damage.resolve()
    else:
      print(f'{target_name} successfully defended against {name}\'s Attack.')

  def get_default_state(self):
    return { 'attack_modifiers': {}, 'damage_modifiers': {}, 'roll': 0, 'target_id': None }

  def get_initiative(self):
    return self.get_score()
  
  def get_is_flanking(self):
    targets_target_id = self.hydrate('target_id').hydrate('planned_action_id').get('target_id')

    return targets_target_id is not self.parent.id

  def get_score(self):
    score = self.get('roll')
    score += sum([modifier for modifier in self.get('attack_modifiers').values()])
    weapon = self.parent.hydrate('weapon_id')
    weapon_attribute_caps = weapon.get('attribute_caps')
    attributes = self.parent.get('attributes')
    score += sum([min(attributes[attr], cap) for attr,cap in weapon_attribute_caps.items()])
    score += sum([modifier for modifier in weapon.get('attack_modifiers').values()])
    targets_target_id = self.hydrate('target_id').hydrate('planned_action_id').get('target_id')

    if self.get_is_flanking():
      score += 2

    return score
