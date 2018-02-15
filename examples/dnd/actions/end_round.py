from engine.action import Action

class EndRound(Action):
  def execute(self, diff):
    if self.game.get('round_number') == 5:
      self.game.set('is_in_progress', False)
