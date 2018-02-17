from engine.request import request
from examples.dnd.actions.move import Move
from examples.dnd.actions.plan import Plan

class PlanMove(Plan):
  def get_is_possible(character):
    return len(character.parent.get('neighbor_ids')) > 0

  def execute(self, diff):
    move = Move(parent=self.parent)
    neighbor_ids = list(self.parent.parent.get('neighbor_ids'))
    target_location_id_args = { 'action_id': move.id, 'num_targets': 1, 'valid_ids': neighbor_ids }
    target_location_ids = request(self, self.parent, 'target_location_ids', args=target_location_id_args)
    target_location_id = target_location_ids[0] if len(target_location_ids) > 0 else None
    move.set('target_location_id', target_location_id)
    self.parent.set('active_ability_id', move.id)
