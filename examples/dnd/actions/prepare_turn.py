from engine.action import Action
from engine.request import request

class PrepareTurn(Action):
  def execute(self, diff):
    ability_id = request(self, self.parent, 'ability_id')
    self.parent.set('active_ability_id', ability_id)

    if ability_id is not None:
      ability = self.hydrate_by_id(ability_id)
      ability.prepare()
