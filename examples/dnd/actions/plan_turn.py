import re
from engine.listener import Listener

text_to_abilities = {
  r'(impotent)?\s*rage': 'PlanImpotentRage',
  r'whistle': 'PlanWhistle',
}

class PlanTurn(Listener):
  def execute(self, diff):
    abilities = self.parent.get('abilities')
    name = self.parent.get('name')
    action_class = None

    while action_class is None:
      action_name = input(f'Enter an action for player {name}: ').lower()

      for matcher in text_to_abilities:
        if re.match(matcher, action_name):
          action_class_name = text_to_abilities[matcher]
          
          if action_class_name in abilities:
            action_class = self.root.entity_classes[action_class_name]
          else:
            print(f'{name} does not have the ability to perform {action_name}.')

          break
      
      if action_class is None:
        print(f'{action_name} does match any known abilities. Options include: {text_to_abilities} Try again.')

    action = action_class(parent=self.parent)
    action.resolve()

  def get_should_react(self, trigger_action, diff, is_preparation):
    return is_preparation and trigger_action.get_name() is 'StartRound'
