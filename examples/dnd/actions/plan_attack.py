from engine.action import Action
from examples.dnd.actions.attack import Attack
from examples.dnd.actions.choose_character_target import ChooseCharacterTarget

class PlanAttack(Action):
  def execute(self, diff):
    attack = Attack(parent=self.parent)
    choose_character_target = ChooseCharacterTarget(parent=self, state={ 'action_id': attack.id })
    choose_character_target.resolve()
    roll = self.parent.request('roll', args={ 'action_id': attack.id })
    attack.set('roll', roll)
    self.parent.set('planned_action_id', attack.id)
