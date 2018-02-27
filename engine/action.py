from engine.base_action import BaseAction
from engine.destroy_entity import DestroyEntity
from engine.diff import Diff

class Action(BaseAction):
  def get_should_self_destruct(self):
    return True

  def resolve(self, diff=Diff()):
    super().resolve(diff)

    if self.get_should_self_destruct():
      game = self.game
      destroy_entity = DestroyEntity(parent=game, state={ 'entity_id': self.id })
      destroy_entity.resolve()
      game.remove_child(destroy_entity)
