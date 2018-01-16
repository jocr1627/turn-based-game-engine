from engine.action import Action
from examples.dnd.actions.character_action import CharacterAction

class Whistle(CharacterAction):
  name = 'Whistle'

  def execute(self):
    name = self.entity.state['name']
    target_name = self.options['target'].state['name']
    print(f'{name} whistled to {target_name}')

    return {}
