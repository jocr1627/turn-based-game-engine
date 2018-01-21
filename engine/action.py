from engine.diff import Diff
from engine.entity import Entity

class Action(Entity):
  def execute(self, diff):
    return {}

  def get_is_valid(self):
    return True

  def handle_listeners(self, diff, is_preparation):
    listener_queue = []

    for listener in self.root.listeners.values():
      if not listener.get_is_cycle() and listener.get_should_react(self, diff, is_preparation):
        listener_queue.append(listener)
    
    listener_queue = sorted(listener_queue, key=lambda listener: listener.get_priority(), reverse=True)

    for listener in listener_queue:
      listener.resolve(diff)

  def resolve(self, diff=Diff()):
    if not self.get_is_valid():
      return
    
    self.root.triggers.append({ 'action': self, 'is_preparation': True })
    self.handle_listeners(diff, True)
    self.root.triggers.pop()

    if not self.get_is_valid():
      return

    self.root.triggers.append({ 'action': self, 'is_preparation': False })
    self.root.start_diff()
    self.execute(diff)
    next_diff = self.root.end_diff()
    self.handle_listeners(next_diff, False)
    self.root.triggers.pop()
