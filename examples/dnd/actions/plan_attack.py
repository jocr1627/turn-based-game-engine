from engine.action import Action
from engine.request import request
from examples.dnd.actions.attack import Attack
from examples.dnd.actions.finalize_attack import FinalizeAttack

class PlanAttack(Action):
  def execute(self, diff):
    attack = Attack(parent=self.parent)
    character_ids = self.game.get('character_ids')
    other_character_ids = [character_id for character_id in character_ids if character_id is not self.parent.id]
    target_character_id_args = { 'action_id': attack.id, 'num_targets': 1, 'valid_ids': other_character_ids }
    target_character_ids = request(self, self.parent, 'target_character_ids', args=target_character_id_args)
    target_character_id = target_character_ids[0] if len(target_character_ids) > 0 else None
    target_character = self.hydrate_by_id(target_character_id)
    attack.set('target_character_id', target_character_id)
    base_roll, modified_roll = request(self, self.parent, 'roll', args={ 'action_id': attack.id, 'roll_type': 'attack' })
    attack.set('base_roll', base_roll)
    attack.set('modified_roll', modified_roll)
    FinalizeAttack(parent=self.parent, state={ 'attack_id': attack.id })
    self.parent.set('planned_action_id', attack.id)
