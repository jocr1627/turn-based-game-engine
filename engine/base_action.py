from engine.diff import Diff
from engine.entity import Entity

class BaseAction(Entity):
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

  def handle_listeners(self, diff, game):
    listener_set = set()
    trigger_types = self.get_types().union([None])

    for trigger_type in trigger_types:
      if trigger_type in game.listeners:
        for listener in game.listeners[trigger_type].values():
          if listener.get_should_react(diff):
            listener_set.add(listener)

    listener_queue = sorted(list(listener_set), key=lambda listener: listener.get_priority(), reverse=True)

    for listener in listener_queue:
      listener.resolve(diff)

  def resolve(self, diff=Diff()):
    if self.game is None or not self.get_is_valid(diff):
      return

    game = self.game
    game.action_stack.push(self)
    game.start_diff()
    self.execute(diff)
    next_diff = game.end_diff()
    self.handle_listeners(next_diff, game)
    game.action_stack.pop()
