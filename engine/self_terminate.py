from engine.base_listener import BaseListener

class SelfTerminate(BaseListener):
  def resolve(self, diff):
    print('doing it', self.parent.get_name())
    self.parent.remove_child(self)

  def get_should_react(self, diff):
    return self.parent.get_should_terminate(diff)
