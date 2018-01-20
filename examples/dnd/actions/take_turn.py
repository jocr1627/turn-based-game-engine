from engine.listener import Listener

class TakeTurn(Listener):
  def execute(self, diff):
    planned_action_id = self.parent.get('planned_action_id')
    planned_action = self.root.descendants[planned_action_id]
    planned_action.resolve()
    
  def get_is_valid(self):
    planned_action_id = self.parent.get('planned_action_id')

    return planned_action_id in self.root.descendants

  def get_priority(self):
    planned_action_id = self.parent.get('planned_action_id')

    if planned_action_id not in self.root.descendants:
      return 0
    else:
      planned_action = self.root.descendants[planned_action_id]
      
      return planned_action.get('initiative')

  def get_should_react(self, trigger_action, diff, is_preparation):
    planned_action_id = self.parent.get('planned_action_id')

    return (
      not is_preparation
      and trigger_action.get_name() is 'StartRound'
    )
