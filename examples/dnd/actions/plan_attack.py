from engine.action import Action
from engine.request import request
from examples.dnd.actions.attack import Attack
from examples.dnd.actions.finalize_attack import FinalizeAttack
from examples.dnd.entities.character import Character

class PlanAttack(Action):
  def execute(self, diff):
    weapon = self.parent.get_weapon()
    attack = Attack(parent=self.parent, state={ 'weapon_id': weapon.id })
    is_ranged = weapon.get('is_ranged')
    location = self.parent.parent
    valid_target_character_ids = [
      entity.id for entity in location.children.values() if isinstance(entity, Character) and entity is not self.parent
    ]
    target_character_id_args = { 'action_id': attack.id, 'num_targets': 1, 'valid_ids': valid_target_character_ids }
    target_character_ids = request(self, self.parent, 'target_character_ids', args=target_character_id_args)
    target_character_id = target_character_ids[0] if len(target_character_ids) > 0 else None
    target_character = self.hydrate_by_id(target_character_id)
    attack.set('target_character_id', target_character_id)
    base_roll, modified_roll = request(self, self.parent, 'roll', args={ 'action_id': attack.id, 'roll_type': 'attack' })
    attack.set('base_roll', base_roll)
    attack.set('modified_roll', modified_roll)
    FinalizeAttack(parent=self.parent, state={ 'attack_id': attack.id })
    self.parent.set('planned_action_id', attack.id)
