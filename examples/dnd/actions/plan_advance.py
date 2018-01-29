from engine.action import Action
from engine.request import request
from examples.dnd.actions.advance import Advance

class PlanAdvance(Action):
  def execute(self, diff):
    advance = Advance(parent=self.parent)
    character_ids = self.root.get('character_ids')
    other_character_ids = [character_id for character_id in character_ids if character_id is not self.parent.id]
    target_character_id_args = { 'action_id': advance.id, 'num_targets': 1, 'valid_ids': other_character_ids }
    target_character_id = request(self.parent, 'target_character_ids', args=target_character_id_args)[0]
    target_character = self.hydrate_by_id(target_character_id)
    advance.set('target_character_id', target_character_id)
    advance.set('original_target_location_id', target_character.parent.id)
    self.parent.set('planned_action_id', advance.id)
