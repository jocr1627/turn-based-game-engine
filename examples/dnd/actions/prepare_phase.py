from engine.action import Action
from engine.request import request

class PreparePhase(Action):
  def execute(self, diff):
    characters = self.game.hydrate('character_ids')

    for character in characters:
      if character.get('is_alive'):
        ability_id = request(self, character, 'ability_id')
        character.set('active_ability_id', ability_id)

        if ability_id is not None:
          ability = self.hydrate_by_id(ability_id)
          ability.prepare()
