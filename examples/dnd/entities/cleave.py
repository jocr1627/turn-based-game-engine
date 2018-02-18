from engine.deep_merge import deep_merge
from examples.dnd.entities.activated_ability import ActivatedAbility
from examples.dnd.entities.melee_attack import MeleeAttack

class Cleave(ActivatedAbility, MeleeAttack):
  matcher = r'^cleave$'

  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      { 'num_targets': 2 }
    )
