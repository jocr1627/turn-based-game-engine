from engine.entity import Entity

class Armor(Entity):
  def __init__(
    self,
    modifier,
    dexterity_cap=None,
    name=None,
    owner=None
  ):
    state = {
      'modifier': modifier,
      'dexterity_cap': dexterity_cap
    }

    if name is not None:
      state['name'] = name

    super().__init__(parent=owner, state=state)
  
  def get_default_state(self):
    return {
      'modifier': 0,
      'dexterity_cap': None,
      'name': self.get_name()
    }
