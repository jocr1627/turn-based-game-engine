from engine.action import Action

class Stun(Action):
  def execute(self, diff):
    self.parent.set('is_stunned', True)
  
  def get_is_valid(self, diff):
    return not self.parent.get('is_stunned')
