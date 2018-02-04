from engine.action import Action
from examples.dnd.actions.attack import Attack
from examples.dnd.actions.choose_character_target import ChooseCharacterTarget

class PlanAttack(Action):
  def execute(self, diff):
    attack = Attack(parent=self.parent)
    choose_character_target = ChooseCharacterTarget(parent=self, state={ 'action_id': attack.id })
    choose_character_target.resolve()
    name = self.parent.get('name')
    roll = None

    while roll is None:
      raw_roll = input(f'Enter {name}\'s roll for Attack: ')

      try:
        roll = int(raw_roll)
      except ValueError:
        print(f'{raw_roll} is not a valid roll.')
    
    attack.set('roll', roll)
    self.parent.set('planned_action_id', attack.id)
