from engine.action import Action

class FinalizePhase(Action):
  def execute(self, diff):
    characters = self.game.get_characters()

    for character in characters:
      ability = character.get_active_ability()

      if ability is not None:
        ability.finalize()
