from examples.dnd.attack_types import AttackTypes
from examples.dnd.entities.weapons.weapon import Weapon

class WoodenSpear(Weapon):
  def __init__(self, owner=None):
    attribute_caps = { 'dexterity': 1, 'strength': 1 }
    dice = { 4: 1 }

    super().__init__(
      dice,
      attack_type=AttackTypes.PIERCING,
      attribute_caps=attribute_caps,
      owner=owner
    )
