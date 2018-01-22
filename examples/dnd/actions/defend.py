from engine.action import Action
from examples.dnd.actions.deal_damage import DealDamage

class Defend(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    roll = None

    while roll is None:
      raw_roll = input(f'Enter {name}\'s roll for Defend: ')

      try:
        roll = int(raw_roll)
      except ValueError:
        print(f'{raw_roll} is not a valid roll.')

    self.set('roll', roll)

  def get_default_state(self):
    return { 'attack_id': None, 'modifiers': {}, 'roll': 0 }

  def get_score(self):
    score = self.get('roll')
    score += sum([modifier for modifier in self.get('modifiers').values()])
    armor = self.parent.hydrate('armor_id')
    score += armor.get('bonus')
    attack_type = self.hydrate('attack_id').parent.hydrate('weapon_id').get('attack_type')
    dexterity_cap = armor.get('dexterity_cap')

    if attack_type is 'physical':
      score += min(self.parent.getIn(['attributes', 'dexterity']), dexterity_cap)
    
    score += sum([modifier for modifier in armor.get('modifiers').values()])
  
    return score
