from engine.base_action import BaseAction

class DestroyEntity(BaseAction):
  def execute(self, diff):
    entity = self.hydrate('entity_id')
    entity.parent.remove_child(entity)
