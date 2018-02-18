from engine.action import Action
from engine.entity import Entity
from examples.dnd.priorities import Priorities

class Ability(Entity):
  parent_alias = 'character'

  def finalize(self):
    return

  def get_initiative(self):
    return Priorities.NO_ROLL_ACTION

  def get_is_possible(self):
    return True

  def validate_parent(self, parent):
    if not parent.is_type('Character'):
      raise ValueError(f'Invalid parent for {self.__class__.__name__}. Expected Character but got {parent.__class__.__name__}.')

  def prepare(self):
    return

  def resolve(self):
    return

class AbilityAction(Action):
  parent_alias = 'ability'

  def validate_parent(self, parent):
    if not parent.is_type('Ability'):
      raise ValueError(f'Invalid parent for {self.__class__.__name__}. Expected Ability but got {parent.__class__.__name__}.')
