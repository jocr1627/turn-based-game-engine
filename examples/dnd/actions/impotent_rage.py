from engine.action import Action
from examples.dnd.actions.character_action import CharacterAction

class ImpotentRage(CharacterAction):
  def execute(self, diff):
    name = self.entity.state.get('name')
    print(f'"ARRRGHH, WHY???!!!" - {name}')

    return {}
