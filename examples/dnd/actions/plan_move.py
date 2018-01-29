from engine.action import Action
from examples.dnd.actions.move import Move

class PlanMove(Action):
  def execute(self, diff):
    move = Move(parent=self.parent)
    neighbor_ids = self.parent.parent.get('neighbor_ids')
    target_location_id_args = { 'action_id': flee.id, 'num_targets': 1, 'valid_ids': neighbor_ids }
    target_location_id = self.parent.request('target_location_ids', args=target_location_id_args)[0]
    flee.set('target_location_id', target_location_id)
    self.parent.set('planned_action_id', move.id)
