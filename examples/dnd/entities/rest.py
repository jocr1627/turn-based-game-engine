from engine.action import Action
from examples.dnd.entities.ability import Ability
from examples.dnd.priorities import Priorities

class ResolveRest(Action):
  def execute(self, diff):
    max_mp = self.parent.parent.get('max_mp')
    self.parent.parent.set('mp', max_mp)

  def get_initiative(self):
    return Priorities.NO_ROLL_ACTION

  def get_is_valid(self, diff):
    return self.parent.parent.get('is_alive')

class Rest(Ability):
  matcher = r'^rest$'

  def get_initiative(self):
    return Priorities.NO_ROLL_ACTION

  def get_is_possible(self):
    return self.parent.get('mp') < self.parent.get('max_mp')

  def resolve(self):
    resolve_rest = ResolveRest(parent=self)
    resolve_rest.resolve()
