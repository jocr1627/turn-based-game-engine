from engine.deep_merge import deep_merge
from engine.request import request
from examples.dnd.actions.decrement_cooldown import DecrementCooldown
from examples.dnd.entities.ability import Ability

class CooldownAbility(Ability):
  def get_cooldown(self, args):
    return 2 if self.get('rank') < 2 else 1
  
  def get_default_children(self):
    return deep_merge(
      super().get_default_children(),
      [DecrementCooldown()]
    )

  def get_default_getters(self):
    return deep_merge(
      super().get_default_getters(),
      { 'cooldown': self.get_cooldown }
    )

  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      { 'remaining_cooldown': 0 }
    )
  
  def get_is_possible(self):
    return self.get('remaining_cooldown') == 0 and super().get_is_possible()

  def resolve(self):
    cooldown = request(self, self, 'cooldown')
    self.set('remaining_cooldown', cooldown)
    super().resolve()
