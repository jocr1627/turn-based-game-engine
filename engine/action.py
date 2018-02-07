from engine.base_action import BaseAction, Phases
from engine.self_terminate import SelfTerminate

class Action(BaseAction):
  def get_default_children(self):
    return [SelfTerminate()]

  def get_should_terminate(self, diff):
    trigger = self.get_trigger()

    return (
      trigger is self.parent
      and trigger.phase is Phases.EXECUTION
    )
