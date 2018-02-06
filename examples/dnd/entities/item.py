from engine.entity import Entity

class Item(Entity):
  def __init__(self, children=[], getters={}, name=None, owner=None, state={}):
    if name is not None:
      state['name'] = name

    super().__init__(children=children, getters=getters, parent=owner, state=state)

  def get_default_state(self):
    return { 'name': self.get_name() }
