from engine.deep_merge import deep_merge
from examples.dnd.entities.activated_ability import ActivatedAbility
from examples.dnd.entities.melee_attack import MeleeAttack

class Cleave(ActivatedAbility, MeleeAttack):
  matcher = r'^cleave$'

  def get_num_targets(self, args):
    return 2 if self.get('rank') < 3 else 3
