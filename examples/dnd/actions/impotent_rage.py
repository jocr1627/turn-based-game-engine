from engine.action import Action
from examples.dnd.actions.character_action import CharacterAction

class ImpotentRage(CharacterAction):
  name = 'ImpotentRage'

  def execute(self):
    name = self.entity.state['name']
    print(f'"ARRRGHH, WHY???!!!" - {name}')

    return {}
