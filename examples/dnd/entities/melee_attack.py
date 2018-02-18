from examples.dnd.entities.attack import Attack

class MeleeAttack(Attack):
  def get_is_possible(self):
    return not self.character.get_weapon().get('is_ranged') and super().get_is_possible()
