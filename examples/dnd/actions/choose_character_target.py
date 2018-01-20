from engine.action import Action

class ChooseCharacterTarget(Action):
  def execute(self, diff):
    character_ids = self.root.get('character_ids')
    characters = [self.root.descendants[character_id] for character_id in character_ids]
    character_names = [character.get('name') for character in characters]
    target_id = None

    while target_id is None:
      target_name = input(f'Enter a target: ').lower()

      for character in characters:
        if character.get('name').lower() == target_name:
          target_id = character.id
      
      if target_id is None:
        print(f'{target_name} is not a known character. Options include: {character_names} Try again.')

    action_id = self.get('action_id')
    action = self.root.descendants[action_id]
    action.set('target_id', target_id)
