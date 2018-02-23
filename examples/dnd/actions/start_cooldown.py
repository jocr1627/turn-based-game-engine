from engine.action import Action

class StartCooldown(Action):
  def execute(self, diff):
    cooldown = request(self, self.parent, 'cooldown')
    self.parent.set('remaining_cooldown', cooldown)
