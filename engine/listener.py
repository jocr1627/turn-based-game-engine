from engine.action import Action

class Listener(Action):
  name = 'Listener'

  def get_is_cycle(self):
    return any(map(lambda trigger: self.parent is trigger['action'].parent and self.name is trigger['action'].name, self.root.triggers))

  def get_priority(self):
    return 0
  
  def get_should_react(self, trigger_action, diff, is_preparation):
    return False
