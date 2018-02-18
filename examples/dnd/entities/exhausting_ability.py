from examples.dnd.entities.cooldown_ability import CooldownAbility

class ExhaustingAbility(CooldownAbility):
  def get_cooldown(self, args):
    return 4 if self.get('rank') < 2 else 3
