from engine.diff import Diff
from engine.entity import Entity

class Phases:
  IDLE = 0
  PREPARATION = 1
  EXECUTION = 2

class Action(Entity):
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
    triggers = self.root.action_stack.stack

    if len(triggers) > 0 and triggers[-1] is self:
      triggers = triggers[0:-1]
    
    return triggers

  def handle_listeners(self, diff):
    listener_queue = []

    for listener in self.root.listeners.values():
      if not listener.get_is_cycle() and listener.get_should_react(diff):
        listener_queue.append(listener)
    
    listener_queue = sorted(listener_queue, key=lambda listener: listener.get_priority(), reverse=True)

    for listener in listener_queue:
      listener.resolve(diff)

  def resolve(self, diff=Diff()):
    if not self.get_is_valid(diff):
      return
    
    self.phase = Phases.PREPARATION
    self.root.action_stack.push(self)

    self.handle_listeners(diff)

    if not self.get_is_valid(diff):
      return

    self.phase = Phases.EXECUTION

    self.root.start_diff()
    self.execute(diff)
    next_diff = self.root.end_diff()

    self.handle_listeners(next_diff)

    self.phase = Phases.IDLE
    self.root.action_stack.pop()
