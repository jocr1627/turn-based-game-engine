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
    roll = self.get('roll')
    attack_score = self.get('score')
    defense_roll = defend.get('roll')
    defense_score = defend.get('score')

    if defense_roll != 20 and roll != 1 and (roll == 20 or attack_score > defense_score):
      is_critical = request(self.parent, 'is_critical', args={ 'roll': roll })
      damage = request(self.parent, 'weapon_damage', args={ 'action_id': self.id, 'is_critical': is_critical })
      deal_damage = DealDamage(parent=target_character, state={ 'damage': damage })
      deal_damage.resolve()
    else:
      print(f'{target_character_name} successfully defended against {name}\'s Attack.')

  def get_default_state(self):
    return { 'roll': None, 'score': None, 'target_character_id': None }

  def get_is_valid(self):
    return self.hydrate('target_character_id').parent is self.parent.parent

  def get_priority(self):
    return normalize_priority(Priorities.STANDARD_ACTION, self.get('score'))
