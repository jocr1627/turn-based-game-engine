from examples.dnd.attack_types import AttackTypes
from examples.dnd.entities.weapons.weapon import Weapon

class ElvenBow(Weapon):
  def __init__(self, owner=None):
    attribute_caps = { 'dexterity': 1 }
    dice = { 6: 1 }

    super().__init__(
      dice,
      attack_type=AttackTypes.PIERCING,
      attribute_caps=attribute_caps,
      owner=owner,
      is_ranged=True
    )
