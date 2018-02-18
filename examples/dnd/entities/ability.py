from engine.entity import Entity
from examples.dnd.priorities import Priorities

class Ability(Entity):
  def __init__(self):
    super().__init__()

  def finalize(self):
    return

  def get_initiative(self):
    return Priorities.NO_ROLL_ACTION

  def get_is_possible(self):
    return True

  def prepare(self):
    return

  def resolve(self):
    return
