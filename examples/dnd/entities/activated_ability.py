from engine.deep_merge import deep_merge
from examples.dnd.entities.mana_expending_ability import ManaExpendingAbility

class ActivatedAbility(ManaExpendingAbility):
  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      { 'mana_cost': 2 }
    )
