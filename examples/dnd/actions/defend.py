from engine.action import Action
from engine.deep_merge import deep_merge
from engine.request import request

class Defend(Action):
  def execute(self, diff):
    base_roll, modified_roll = request(self, self.parent, 'roll', args={ 'action_id': self.id, 'roll_type': 'defend' })
    physical_defense_modifier = request(self, self.parent, 'physical_defense_modifier')
    self.set('base_roll', base_roll)
    self.set('modified_roll', modified_roll)
    self.set('score', modified_roll + physical_defense_modifier)

  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      {
        'attack_id': None,
        'base_roll': None,
        'modified_roll': None,
        'score': None
      }
    )
