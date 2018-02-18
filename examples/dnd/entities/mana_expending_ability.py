from engine.deep_merge import deep_merge
from examples.dnd.actions.spend_mana import SpendMana
from examples.dnd.entities.ranked_ability import RankedAbility

class ManaExpendingAbility(RankedAbility):
  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      { 'mana_cost': 0 }
    )
  
  def get_is_possible(self):
    return self.character.get('mp') >= self.get('mana_cost') and super().get_is_possible()

  def resolve(self):
    mana_cost = self.get('mana_cost')
    spend_mana = SpendMana(parent=self.character, state={ 'mana': mana_cost })
    spend_mana.resolve()
    super().resolve()
