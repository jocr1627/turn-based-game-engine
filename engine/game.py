from engine.action_stack import ActionStack
from engine.entity import Entity

class Game(Entity):
  def __init__(self, children=[], getters={}, state={}):
    self.action_stack = ActionStack()
    self.descendants = {}
    self.diffs = []
    self.listeners = {}

    super().__init__(children=children, game=self, getters=getters, state=state)

  def run(self):
    return
