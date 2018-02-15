from engine.action import Action
from engine.request import request
from examples.dnd.actions.advance import Advance
from examples.dnd.entities.character import Character

class PlanAdvance(Action):
  def execute(self, diff):
    advance = Advance(parent=self.parent)
    valid_locations = [self.parent.parent]
    valid_locations += self.parent.parent.hydrate('neighbor_ids')
    valid_character_ids = []

    for location in valid_locations:
      valid_character_ids += [
        entity.id for entity in location.children.values()
        if isinstance(entity, Character) and entity is not self.parent
      ]

    target_character_id_args = { 'action_id': advance.id, 'num_targets': 1, 'valid_ids': valid_character_ids }
    target_character_ids = request(self, self.parent, 'target_character_ids', args=target_character_id_args)
    target_character_id = target_character_ids[0] if len(target_character_ids) > 0 else None
    target_character = self.hydrate_by_id(target_character_id)
    advance.set('target_character_id', target_character_id)
    advance.set('original_target_location_id', target_character.parent.id)
    self.parent.set('planned_action_id', advance.id)
