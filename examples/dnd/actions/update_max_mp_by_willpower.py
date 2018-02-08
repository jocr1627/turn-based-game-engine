from engine.base_entity_listener import BaseEntityListener

class UpdateMaxMpByWillpower(BaseEntityListener):
  def execute(self, diff):
    willpower,new_willpower = diff.get_in(['state', self.parent.id, 'attributes', 'willpower'])
    difference = new_willpower - willpower
    self.parent.update('max_mp', lambda max_mp: max(max_mp + difference, 0))

  def get_should_react(self, diff):
    return diff.has_in(['state', self.parent.id, 'attributes', 'willpower'])
