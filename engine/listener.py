from engine.base_action import BaseAction
from engine.deep_merge import deep_merge

class Listener(BaseAction):
  def __init__(self, trigger_types=[], **args):
    super().__init__(**args)
    self.trigger_types = deep_merge(self.get_default_trigger_types(), trigger_types)

  def get_default_trigger_types(self):
    return []

  def get_priority(self):
    return 0

  def get_should_react(self, diff):
    return True
