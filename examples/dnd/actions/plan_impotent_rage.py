from engine.action import Action
from examples.dnd.actions.impotent_rage import ImpotentRage

class PlanImpotentRage(Action):
  def execute(self, diff):
    impotent_rage = ImpotentRage(parent=self.parent)
    name = self.parent.get('name')
    initiative = None

    while initiative is None:
      roll = input(f'Enter {name}\'s roll for Impotent Rage: ')

      try:
        initiative = int(roll)
      except ValueError:
        print(f'{roll} is not a valid roll.')
      
    impotent_rage.set('initiative', initiative)
    self.parent.set('planned_action_id', impotent_rage.id)
