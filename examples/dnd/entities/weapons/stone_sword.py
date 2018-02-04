from examples.dnd.entities.weapons.weapon import Weapon

class StoneSword(Weapon):
  def __init__(self, owner=None):
    attribute_caps = { 'strength': 1 }
    dice = { 6: 1 }
    super().__init__(dice, attribute_caps=attribute_caps, owner=owner)
