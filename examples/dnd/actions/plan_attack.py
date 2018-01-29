from engine.action import Action
from engine.request import request
from examples.dnd.actions.attack import Attack

class PlanAttack(Action):
  def execute(self, diff):
    attack = Attack(parent=self.parent)
    character_ids = self.root.get('character_ids')
    other_character_ids = [character_id for character_id in character_ids if character_id is not self.parent.id]
    target_character_id_args = { 'action_id': attack.id, 'num_targets': 1, 'valid_ids': other_character_ids }
    target_character_id = request(self.parent, 'target_character_ids', args=target_character_id_args)[0]
    target_character = self.hydrate_by_id(target_character_id)
    attack.set('target_character_id', target_character_id)
    roll = request(self.parent, 'roll', args={ 'action_id': attack.id })
    attack.set('roll', roll)
    weapon_attack_modifier = request(self.parent, 'weapon_attack_modifier')
    is_flanking = request(self.parent, 'is_flanking', args={ 'target_character_id': target_character_id })
    score = roll + weapon_attack_modifier

    if is_flanking:
      score += 2

    attack.set('score', score)
    self.parent.set('planned_action_id', attack.id)
