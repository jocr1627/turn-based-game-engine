from engine.action import Phases
from engine.base_entity_listener import BaseEntityListener

class TakeTurn(BaseEntityListener):
  def execute(self, diff):
    planned_action = self.parent.hydrate('planned_action_id')
    self.parent.set('planned_action_id', None)
    planned_action.resolve()
    
  def get_is_valid(self, diff):
    return (
      self.parent.hydrate('planned_action_id') is not None
      and self.parent.get('is_alive')
    )

  def get_priority(self):
    planned_action = self.parent.hydrate('planned_action_id')
    
    return planned_action.get_priority() if planned_action is not None else 0

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.phase is Phases.EXECUTION
      and trigger.get_name() is 'StartRound'
    )
