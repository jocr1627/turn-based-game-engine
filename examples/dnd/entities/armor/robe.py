from examples.dnd.entities.armor.armor import Armor

class Robe(Armor):
  def __init__(self, owner=None):
    super().__init__(1, dexterity_cap=1, owner=owner)
