from engine.listener import Listener

class DestroyEntity(Listener):
  def execute(self, diff):
    self.game.garbage.add(self.parent.id)
