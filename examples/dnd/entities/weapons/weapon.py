from engine.entity import Entity

class Weapon(Entity):
  def __init__(
    self,
    dice,
    attack_modifiers={},
    attack_type='physical',
    attribute_caps={},
    damage_modifiers={},
    name=None,
    owner=None
  ):
    state = {
      'attack_modifiers': attack_modifiers,
      'attack_type': attack_type,
      'attribute_caps': attribute_caps,
      'damage_modifiers': damage_modifiers,
      'dice': dice
    }

    if name is not None:
      state['name'] = name

    super().__init__(parent=owner, state=state)
  
  def get_default_state(self):
    return {
      'attack_modifiers': {},
      'attack_type': 'physical',
      'attribute_caps': {},
      'damage_modifiers': {},
      'dice': {},
      'name': self.get_name()
    }
