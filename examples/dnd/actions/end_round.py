from engine.action import Action

class EndRound(Action):
  def execute(self, diff):
    characters = self.game.get_characters()

    for character in characters:
      character.clear_round_state()

    if self.game.get_round_number() == 5:
      self.game.end()
