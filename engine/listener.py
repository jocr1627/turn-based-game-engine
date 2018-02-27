from engine.action import Action
from engine.deep_merge import deep_merge

class Listener(Action):
  def __init__(self, trigger_types=[], **args):
    self.trigger_types = set(deep_merge(self.get_default_trigger_types(), trigger_types))
    super().__init__(**args)

  def get_default_trigger_types(self):
    return []

  def get_priority(self):
    return 0
  
  def get_should_react(self, diff):
    return True
  
  def get_should_self_destruct(self):
    return False
