from examples.dnd.entities.ability import Ability, AbilityAction
from examples.dnd.priorities import Priorities

class Rest(Ability):
  matcher = r'^rest$'

  def get_initiative(self):
    return Priorities.NO_ROLL_ACTION

  def get_is_possible(self):
    return self.character.get('mp') < self.character.get('max_mp')

  def resolve(self):
    rest = Rest(parent=self.character)
    rest.resolve()
