from engine.action import Action
from examples.dnd.actions.attack import Attack

class PlanAttack(Action):
  def execute(self, diff):
    attack = Attack(parent=self.parent)
    character_ids = self.root.get('character_ids')
    other_character_ids = [character_id for character_id in character_ids if character_id is not self.parent.id]
    target_character_id_args = { 'action_id': advance.id, 'num_targets': 1, 'valid_ids': other_character_ids }
    target_character_id = self.request('target_character_ids', args=target_character_id_args)[0]
    target_character = self.hydrate_by_id(target_character_id)
    attack.set('target_character_id', target_character_id)
    roll = self.parent.request('roll', args={ 'action_id': attack.id })
    attack.set('roll', roll)
    self.parent.set('planned_action_id', attack.id)
