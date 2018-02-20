from engine.base_action import BaseAction
from engine.destroy_entity import DestroyEntity
from engine.diff import Diff

class Action(BaseAction):
  is_self_destructive = True

  def resolve(self, diff=Diff()):
    super().resolve(diff)

    if self.is_self_destructive:
      game = self.game
      destroy_entity = DestroyEntity(parent=game, state={ 'entity_id': self.id })
      destroy_entity.resolve()
      game.remove_child(destroy_entity)
