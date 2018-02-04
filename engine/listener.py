from engine.action import Action

class Listener(Action):
  should_allow_cycles = False

  def get_is_cycle(self):
    return not self.should_allow_cycles and self.root.action_stack.is_cycle(self)

  def get_priority(self):
    return 0
  
  def get_should_react(self, diff):
    return False
