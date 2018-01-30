from engine.listener import Listener
from engine.request import request

class FinalizeAttack(Listener):
  def execute(self, diff):
    attack = self.hydrate('attack_id')
    roll = attack.get('roll')
    target_character_id = attack.get('target_character_id')
    weapon_attack_modifier = request(self.parent, 'weapon_attack_modifier')
    is_flanking = request(self.parent, 'is_flanking', args={ 'target_character_id': target_character_id })
    score = roll + weapon_attack_modifier

    if is_flanking:
      score += 2

    attack.set('score', score)

  def get_should_react(self, trigger_action, diff, is_preparation):
    return not is_preparation and trigger_action.get_name() is 'PlanPhase'
