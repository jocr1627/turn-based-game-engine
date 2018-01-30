from engine.action import Action
from engine.request import request
from examples.dnd.actions.move import Move

class PlanMove(Action):
  def execute(self, diff):
    move = Move(parent=self.parent)
    neighbor_ids = list(self.parent.parent.get('neighbor_ids'))
    target_location_id_args = { 'action_id': move.id, 'num_targets': 1, 'valid_ids': neighbor_ids }
    target_location_ids = request(self.parent, 'target_location_ids', args=target_location_id_args)
    target_location_id = target_location_ids[0] if len(target_location_ids) > 0 else None
    move.set('target_location_id', target_location_id)
    self.parent.set('planned_action_id', move.id)
