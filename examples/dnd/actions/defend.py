from engine.action import Action
from engine.request import request
from examples.dnd.actions.deal_damage import DealDamage

class Defend(Action):
  def execute(self, diff):

    
    roll = request(self.parent, 'roll', args={ 'action_id': self.id })
    self.set('roll', roll)
    physical_defense_modifier = request(self.parent, 'physical_defense_modifier')
    self.set('score', roll + physical_defense_modifier)

  def get_default_state(self):
    return { 'attack_id': None, 'roll': None, 'score': None }
