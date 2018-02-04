from examples.dnd.entities.armor.armor import Armor

class IronArmor(Armor):
  def __init__(self, owner=None):
    super().__init__(2, dexterity_cap=0, owner=owner)
