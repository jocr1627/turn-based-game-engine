from engine.action import Action
from examples.dnd.actions.deal_damage import DealDamage

class Defend(Action):
  def execute(self, diff):
    roll = self.parent.request('roll', args={ 'action_id': self.id })
    self.set('roll', roll)
    physical_defense_modifier = self.parent.request('physical_defense_modifier')
    self.set('score', roll + physical_defense_modifier)

  def get_default_state(self):
    return { 'attack_id': None, 'roll': None, 'score': None }
