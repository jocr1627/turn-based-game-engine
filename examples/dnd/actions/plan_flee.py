from engine.request import request
from examples.dnd.actions.flee import Flee
from examples.dnd.actions.plan import Plan
from examples.dnd.entities.character import Character
from examples.dnd.utils.get_characters_in_range import get_characters_in_range

class PlanFlee(Plan):
  def get_is_possible(character):
    return len(get_characters_in_range(character.parent, 1)) > 0

  def execute(self, diff):
    flee = Flee(parent=self.parent)
    valid_locations = [self.parent.parent]
    valid_locations += self.parent.parent.hydrate('neighbor_ids')
    valid_character_ids = []

    for location in valid_locations:
      valid_character_ids += [
        entity.id for entity in location.children.values()
        if isinstance(entity, Character) and entity is not self.parent
      ]

    target_character_id_args = { 'action_id': flee.id, 'num_targets': 1, 'valid_ids': valid_character_ids }
    target_character_ids = request(self, self.parent, 'target_character_ids', args=target_character_id_args)
    target_character_id = target_character_ids[0] if len(target_character_ids) > 0 else None
    flee.set('target_character_id', target_character_id)
    target_character = self.hydrate_by_id(target_character_id)
    current_target_location_id = target_character.parent.id
    neighbor_ids = self.parent.parent.get('neighbor_ids')
    valid_location_ids = [location_id for location_id in neighbor_ids if location_id is not current_target_location_id]
    target_location_id_args = { 'action_id': flee.id, 'num_targets': 1, 'valid_ids': valid_location_ids }
    target_location_ids = request(self, self.parent, 'target_location_ids', args=target_location_id_args)
    target_location_id = target_location_ids[0] if len(target_location_ids) > 0 else None
    flee.set('target_location_id', target_location_id)
    self.parent.set('planned_action_id', flee.id)
