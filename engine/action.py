from engine.base_entity_action import BaseEntityAction, Phases
from engine.self_terminate import SelfTerminate

class Action(BaseEntityAction):
  def get_default_children(self):
    return [SelfTerminate()]

  def get_should_terminate(self, diff):
    return (
      self is self.game.action_stack.stack[-1]
      and self.phase is Phases.EXECUTION
    )
