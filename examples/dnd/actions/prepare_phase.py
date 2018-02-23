from engine.action import Action

class PreparePhase(Action):
  def execute(self, diff):
    characters = self.game.get_characters()

    for character in characters:
      if character.get('is_alive'):
        character.prepare_turn()
