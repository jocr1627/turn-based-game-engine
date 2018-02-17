from engine.action import Action

class FinalizePhase(Action):
  def execute(self, diff):
    characters = self.game.hydrate('character_ids')

    for character in characters:
      ability = character.hydrate('active_ability_id')

      if ability is not None:
        ability.finalize()
