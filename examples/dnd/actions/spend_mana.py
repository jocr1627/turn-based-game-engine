from engine.action import Action

class SpendMana(Action):
  def execute(self, diff):
    mana = self.get('mana')
    self.parent.update('mp', lambda mp: max(mp - mana, 0))

  def get_is_valid(self, diff):
    mana = self.get('mana')

    return mana > 0 and self.parent.get('mp') >= mana
