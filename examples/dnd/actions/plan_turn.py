from engine.action import Action

class PlanTurn(Action):
  name = 'PlanTurn'

  def execute(self):
    actions = self.entity.state.get('actions')
    name = self.entity.state.get('name')
    action_name = input(f'Enter an action for player {name}: ').lower()
    diffs = {}

    if action_name in actions:
      action = actions[action_name](self.game, self.entity)
      action.resolve()
      initiative = int(input(f'Enter initiative roll for {name}: '))
      initiative += self.entity.state.get('charisma')
      diffs = self.entity.state.set('initiative', initiative)
    else:
      print('I ain\'t got that yo')

    return diffs

  def get_should_react(self, trigger_action, is_preparation):
    return is_preparation and trigger_action.name is 'StartRound'
