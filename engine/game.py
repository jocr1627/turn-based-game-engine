from engine.action import Phases
from engine.action_stack import ActionStack
from engine.entity import Entity

class Game(Entity):
  def __init__(self, children=[], getters={}, state={}):
    self.action_stack = ActionStack()
    self.descendants = {}
    self.diffs = []
    self.garbage = set()
    self.listeners = {}

    super().__init__(children=children, game=self, getters=getters, state=state)

  def collect_garbage(self):
    collected_ids = set()

    for entity_id in self.garbage:
      entity = self.hydrate_by_id(entity_id)

      if not entity.is_type('Action') or entity.phase is Phases.IDLE:
        entity.parent.remove_child(entity)
        collected_ids.add(entity_id)
      
    self.garbage = self.garbage.difference(collected_ids)

  def run(self):
    return
