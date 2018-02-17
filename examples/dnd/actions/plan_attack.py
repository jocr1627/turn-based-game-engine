from engine.request import request
from examples.dnd.actions.attack import Attack
from examples.dnd.actions.finalize_attack import FinalizeAttack
from examples.dnd.actions.plan import Plan
from examples.dnd.entities.character import Character
from examples.dnd.utils.get_characters_in_range import get_characters_in_range

class PlanAttack(Plan):
  def get_is_possible(character):
    max_range = -1 if character.get_weapon().get('is_ranged') else 0

    return len(get_characters_in_range(character.parent, max_range)) > 0

  def execute(self, diff):
    weapon = self.parent.get_weapon()
    attack = Attack(parent=self.parent, state={ 'weapon_id': weapon.id })
    valid_locations = [self.parent.parent]

    if weapon.get('is_ranged'):
      region = self.parent.parent.parent
      valid_locations = region.children.values()

      for neighbor in region.hydrate('neighbor_ids'):
        valid_locations += neighbor.children.values()
    
    valid_target_character_ids = []

    for location in valid_locations:
      valid_target_character_ids += [
        entity.id for entity in location.children.values()
        if isinstance(entity, Character) and entity is not self.parent
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
    self.parent.set('active_ability_id', attack.id)
