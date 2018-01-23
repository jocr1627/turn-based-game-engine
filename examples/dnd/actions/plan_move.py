from engine.action import Action
from examples.dnd.actions.choose_location_target import ChooseLocationTarget
from examples.dnd.actions.move import Move

class PlanMove(Action):
  def execute(self, diff):
    move = Move(parent=self.parent)
    choose_location_target = ChooseLocationTarget(parent=self, state={ 'action_id': move.id })
    choose_location_target.resolve()
    self.parent.set('planned_action_id', move.id)
