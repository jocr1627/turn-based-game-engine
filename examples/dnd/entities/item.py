from engine.deep_merge import deep_merge
from engine.entity import Entity

class Item(Entity):
  def __init__(self, children=[], getters={}, name=None, owner=None, state={}):
    if name is not None:
      state['name'] = name

    super().__init__(children=children, getters=getters, parent=owner, state=state)

  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      { 'name': self.get_name() }
    )
