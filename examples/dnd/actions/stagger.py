from engine.action import Action

class Stagger(Action):
  def execute(self, diff):
    self.parent.set('is_staggered', True)
  
  def get_is_valid(self, diff):
    return not self.parent.get('is_staggered')