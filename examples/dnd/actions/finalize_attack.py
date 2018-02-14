from engine.action import Phases
from engine.listener import Listener
from engine.request import request

class FinalizeAttack(Listener):
  def execute(self, diff):
    attack = self.hydrate('attack_id')
    modified_roll = attack.get('modified_roll')
    target_character_id = attack.get('target_character_id')
    weapon_id = attack.get('weapon_id')
    weapon_attack_modifier = request(self, self.parent, 'weapon_attack_modifier', args={ 'weapon_id': weapon_id })
    is_flanking = request(self, self.parent, 'is_flanking', args={ 'target_character_id': target_character_id })
    score = modified_roll + weapon_attack_modifier

    if is_flanking:
      score += 2

    attack.set('score', score)

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return trigger.phase is Phases.EXECUTION and trigger.get_name() is 'PlanPhase'
