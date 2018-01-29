from engine.action import Action
from engine.request import request
from examples.dnd.actions.flee import Flee

class PlanFlee(Action):
  def execute(self, diff):
    flee = Flee(parent=self.parent)
    character_ids = self.root.get('character_ids')
    other_character_ids = [character_id for character_id in character_ids if character_id is not self.parent.id]
    target_character_id_args = { 'action_id': flee.id, 'num_targets': 1, 'valid_ids': other_character_ids }
    target_character_id = request(self.parent, 'target_character_ids', args=target_character_id_args)[0]
    flee.set('target_character_id', target_character_id)
    target_character = self.hydrate_by_id(target_character_id)
    current_target_location_id = target_character.parent.id
    neighbor_ids = self.parent.parent.get('neighbor_ids')
    valid_location_ids = [location_id for location_id in neighbor_ids if location_id is not current_target_location_id]
    target_location_id_args = { 'action_id': flee.id, 'num_targets': 1, 'valid_ids': valid_location_ids }
    target_location_id = request(self.parent, 'target_location_ids', args=target_location_id_args)[0]
    flee.set('target_location_id', target_location_id)
    self.parent.set('planned_action_id', flee.id)
