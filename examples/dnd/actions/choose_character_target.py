from engine.action import Action
from examples.dnd.actions.character_action import CharacterAction

class ChooseCharacterTarget(CharacterAction):
  name = 'ChooseCharacterTarget'

  def execute(self, diff, options):
    target_name = input(f'Enter a target: ').lower()
    # assuming all children are characters (true so far)
    target = None
    for character in self.game.children.values():
      if character.state.get('name').lower() == target_name:
        target = character

    action = self.options['action']
    old_target = action.options['target'] if 'target' in action.options else None
    action.options['target'] = target

    # TODO: better key. Should actions get ids as well?
    return { action.name: { 'target': (old_target, target) } }
