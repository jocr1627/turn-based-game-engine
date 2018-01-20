from engine.action import Action
from examples.dnd.actions.character_action import CharacterAction

class Whistle(CharacterAction):
  def execute(self, diff):
    name = self.entity.state.get('name')
    target_name = self.options['target'].state.get('name')
    print(f'{name} whistled to {target_name}')

    return {}
