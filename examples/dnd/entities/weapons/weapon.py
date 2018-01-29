from engine.entity import Entity

class Weapon(Entity):
  def __init__(
    self,
    dice,
    attack_modifier=0,
    attack_type='physical',
    attribute_caps={},
    damage_modifier=0,
    name=None,
    owner=None
  ):
    state = {
      'attack_modifier': attack_modifier,
      'attack_type': attack_type,
      'attribute_caps': attribute_caps,
      'damage_modifier': damage_modifier,
      'dice': dice
    }

    if name is not None:
      state['name'] = name

    super().__init__(parent=owner, state=state)
  
  def get_default_state(self):
    return {
      'attack_modifier': 0,
      'attack_type': 'physical',
      'attribute_caps': {},
      'damage_modifier': 0,
      'dice': {},
      'name': self.get_name()
    }
