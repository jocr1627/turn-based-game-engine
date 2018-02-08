from engine.base_entity_listener import BaseEntityListener

class SelfTerminate(BaseEntityListener):
  def resolve(self, diff):
    self.parent.parent.remove_child(self.parent)

  def get_should_react(self, diff):
    return self.parent.get_should_terminate(diff)
