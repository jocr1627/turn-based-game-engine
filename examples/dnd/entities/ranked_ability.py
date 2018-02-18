from engine.deep_merge import deep_merge
from examples.dnd.entities.ability import Ability

class RankedAbility(Ability):
  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      { 'rank': 1 }
    )
