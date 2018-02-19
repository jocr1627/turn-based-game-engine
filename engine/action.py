from engine.base_action import BaseAction, Phases
from engine.deep_merge import deep_merge
from engine.destroy_entity import DestroyEntity

class DestroyAction(DestroyEntity):
  def get_should_react(self, diff):
    return self.get_trigger() is self.parent

class Action(BaseAction):
  def get_default_children(self):
    return deep_merge(
      super().get_default_children(),
      [DestroyAction(trigger_types=[(self.get_name(), Phases.EXECUTION)])]
    )
