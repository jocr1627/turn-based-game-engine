from engine.base_entity_listener import BaseEntityListener

class SelfTerminate(BaseEntityListener):
  def resolve(self, diff):
    self.game.garbage.add(self.parent.id)

  def get_should_react(self, diff):
    return self.parent.get_should_terminate(diff)
