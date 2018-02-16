from engine.request import request
from examples.dnd.actions.advance import Advance
from examples.dnd.actions.plan import Plan
from examples.dnd.entities.character import Character
from examples.dnd.utils.get_characters_in_range import get_characters_in_range

class PlanAdvance(Plan):
  def get_is_possible(character):
    return len(get_characters_in_range(character.parent, 1)) > 0

  def execute(self, diff):
    advance = Advance(parent=self.parent)
    valid_character_ids = get_characters_in_range(self.parent, 1)
    target_character_id_args = { 'action_id': advance.id, 'num_targets': 1, 'valid_ids': valid_character_ids }
    target_character_ids = request(self, self.parent, 'target_character_ids', args=target_character_id_args)
    target_character_id = target_character_ids[0] if len(target_character_ids) > 0 else None
    target_character = self.hydrate_by_id(target_character_id)
    advance.set('target_character_id', target_character_id)
    advance.set('original_target_location_id', target_character.parent.id)
    self.parent.set('planned_action_id', advance.id)
