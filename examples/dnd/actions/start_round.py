from engine.action import Action

class StartRound(Action):
  def execute(self, diff):
    round_number = self.game.get('round_number')
    self.game.set('round_number', round_number + 1)
