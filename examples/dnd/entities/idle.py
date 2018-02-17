from examples.dnd.entities.ability import Ability
from examples.dnd.priorities import Priorities

class Idle(Ability):
  matcher = r'idle'

  def get_initiative(slef):
    return Priorities.IDLE
