from engine.action import Action
from examples.dnd.actions.whistle import Whistle
from examples.dnd.actions.choose_character_target import ChooseCharacterTarget

class PlanWhistle(Action):
  def execute(self, diff):
    whistle = Whistle(parent=self.parent)
    choose_character_target = ChooseCharacterTarget(parent=self, state={ 'action_id': whistle.id })
    choose_character_target.resolve()
    name = self.parent.get('name')
    initiative = None

    while initiative is None:
      roll = input(f'Enter {name}\'s roll for Whistle: ')

      try:
        initiative = int(roll)
      except ValueError:
        print(f'{roll} is not a valid roll.')
      
    whistle.set('initiative', initiative)
    self.parent.set('planned_action_id', whistle.id)
