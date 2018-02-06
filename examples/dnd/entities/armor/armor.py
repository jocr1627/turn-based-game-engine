from examples.dnd.entities.item import Item

class Armor(Item):
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

    super().__init__(name=name, owner=owner, state=state)
  
  def get_default_state(self):
    return {
      'modifier': 0,
      'dexterity_cap': None,
    }
