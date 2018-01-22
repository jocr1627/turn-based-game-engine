from engine.action import Action
from examples.dnd.actions.choose_character_target import ChooseCharacterTarget
from examples.dnd.actions.choose_location_target import ChooseLocationTarget
from examples.dnd.actions.flee import Flee

class PlanFlee(Action):
  def execute(self, diff):
    flee = Flee(parent=self.parent)
    choose_character_target = ChooseCharacterTarget(parent=self, state={ 'action_id': flee.id })
    choose_character_target.resolve()
    choose_location_target = ChooseLocationTarget(parent=self, state={ 'action_id': flee.id })
    choose_location_target.resolve()
    self.parent.set('planned_action_id', flee.id)
