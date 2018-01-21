from engine.action import Action
from examples.dnd.actions.choose_character_target import ChooseCharacterTarget
from examples.dnd.actions.choose_location_target import ChooseLocationTarget
from examples.dnd.actions.advance import Advance

class PlanAdvance(Action):
  def execute(self, diff):
    advance = Advance(parent=self.parent, state={ 'initiative': -1 })
    choose_character_target = ChooseCharacterTarget(parent=self, state={ 'action_id': advance.id })
    choose_character_target.resolve()
    advance.set('original_target_location_id', advance.hydrate('target_id').parent.id)
    self.parent.set('planned_action_id', advance.id)
