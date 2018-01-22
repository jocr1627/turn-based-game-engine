from engine.entity import Entity

class Armor(Entity):
  def __init__(
    self,
    bonus,
    modifiers={},
    dexterity_cap=0,
    name=None,
    owner=None
  ):
    state = {
      'bonus': bonus,
      'dexterity_cap': dexterity_cap,
      'modifiers': modifiers
    }

    if name is not None:
      state['name'] = name

    super().__init__(parent=owner, state=state)
  
  def get_default_state(self):
    return {
      'bonus': 0,
      'dexterity_cap': 0,
      'modifiers': {},
      'name': self.get_name()
    }
