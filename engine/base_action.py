from engine.diff import Diff
from engine.entity import Entity

class Phases:
  IDLE = 'IDLE'
  PREPARATION = 'PREPARATION'
  EXECUTION = 'EXECUTION'

class BaseAction(Entity):
  def __init__(self, **args):
    super().__init__(**args)
    self.phase = Phases.IDLE

  def execute(self, diff):
    return {}

  def get_is_valid(self, diff):
    return True

  def get_trigger(self):
    triggers = self.get_triggers()

    return triggers[-1] if len(triggers) > 0 else None

  def get_triggers(self):
    triggers = self.game.action_stack.stack

    if len(triggers) > 0 and triggers[-1] is self:
      triggers = triggers[0:-1]
    
    return triggers

  def handle_listeners(self, diff):
    listener_set = set()
    trigger_types = [None] + [(entity_type, self.phase) for entity_type in self.get_types()]

    for trigger_type in trigger_types:
      if trigger_type in self.game.listeners:
        for listener in self.game.listeners[trigger_type].values():
          if listener.get_should_react(diff):
            listener_set.add(listener)

    listener_queue = sorted(list(listener_set), key=lambda listener: listener.get_priority(), reverse=True)

    for listener in listener_queue:
      listener.resolve(diff)

  def resolve(self, diff=Diff()):
    if not self.get_is_valid(diff):
      return
    
    self.phase = Phases.PREPARATION
    self.game.action_stack.push(self)

    self.handle_listeners(diff)

    if not self.get_is_valid(diff):
      return

    self.phase = Phases.EXECUTION

    self.game.start_diff()
    self.execute(diff)
    next_diff = self.game.end_diff()

    self.handle_listeners(next_diff)

    self.phase = Phases.IDLE
    self.game.action_stack.pop()
    self.game.collect_garbage()
