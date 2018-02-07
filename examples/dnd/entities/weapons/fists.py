from examples.dnd.attack_types import AttackTypes
from examples.dnd.entities.weapons.weapon import Weapon

class Fists(Weapon):
  def __init__(self, owner=None):
    attribute_caps = { 'strength': None }
    dice = { 4: 1 }

    super().__init__(
      dice,
      attack_type=AttackTypes.BLUNT,
      attribute_caps=attribute_caps,
      owner=owner
    )
