from engine.action import Action
from examples.dnd.actions.choose_location_target import ChooseLocationTarget
from examples.dnd.actions.flee import Flee

class PlanFlee(Action):
  def execute(self, diff):
    flee = Flee(parent=self.parent)
    character_ids = self.root.get('character_ids')
    other_character_ids = [character_id for character_id in character_ids if character_id is not self.parent.id]
    target_character_id_args = { 'action_id': advance.id, 'num_targets': 1, 'valid_ids': other_character_ids }
    target_character_id = self.parent.request('target_character_ids', args=target_character_id_args)[0]
    target_character = self.hydrate_by_id(target_character_id)
    flee.set('target_character_id', target_character_id)
    choose_location_target = ChooseLocationTarget(parent=self, state={ 'action_id': flee.id })
    choose_location_target.resolve()
    self.parent.set('planned_action_id', flee.id)
