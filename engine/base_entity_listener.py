from engine.base_entity_action import BaseEntityAction
from engine.base_listener import BaseListener

class BaseEntityListener(BaseListener, BaseEntityAction):
  should_allow_cycles = False

  def get_is_cycle(self):
    return not self.should_allow_cycles and self.game.action_stack.is_cycle(self)

  def get_priority(self):
    return 0
  
  def get_should_react(self, diff):
    return False
