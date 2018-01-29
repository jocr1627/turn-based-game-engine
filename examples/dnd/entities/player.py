from examples.dnd.entities.character import Character

text_to_abilities = {
  r'advance': 'PlanAdvance',
  r'attack': 'PlanAttack',
  r'equip': 'PlanEquip',
  r'flee': 'PlanFlee',
  r'move': 'PlanMove'
}

class Player(Character):
  def get_plan_action_class_name(self, args):
    abilities = self.get('abilities')
    name = self.get('name')
    action_class_name = None

    while action_class_name is None:
      action_name = input(f'Enter an action for player {name}: ').lower()
      is_match_found = False

      for matcher in text_to_abilities:
        if re.match(matcher, action_name):
          is_match_found = True
          
          if text_to_abilities[matcher] in abilities:
            action_class_name = text_to_abilities[matcher]
          else:
            print(f'{name} does not have the ability to perform {action_name}.')

          break
      
      if not is_match_found:
        print(f'{action_name} does match any known abilities. Options include: {text_to_abilities} Try again.')
    
    return action_class_name

  def get_roll(self, args):
    action_id = args['action_id']
    action = self.hydrate_by_id(action_id)
    action_name = action.get_name()
    name = self.get('name')
    roll = None

    while roll is None:
      raw_roll = input(f'Enter {name}\'s roll for {action_name}: ')

      try:
        roll = int(raw_roll)
      except ValueError:
        print(f'{raw_roll} is not a valid roll.')

    return roll

  def get_target_character_ids(self, args):
    action_id = args['action_id']
    action = self.hydrate_by_id(action_id)
    action_name = action.get_name()
    num_targets = args['num_targets']
    valid_ids = args['valid_ids']
    valid_characters = [self.hydrate_by_id(character_id) for character_id in valid_ids]
    valid_character_ids_by_name = { character.get('name').lower(): character.id for character in valid_characters }
    name = self.get('name')
    target_character_ids = []

    for i in range(num_targets):
      target_character_id = None

      while target_character_id is None:
        target_character_name = input(f'Enter a target character for {name}\'s {action_name}: ').lower()

        if target_character_name in valid_character_ids_by_name:
          target_character_id = valid_character_ids_by_name[target_character_name]
        elif targ
        else:
          print(f'{target_character_name} is not a valid target character. Options include: {list(valid_character_ids_by_name.keys())} Try again.')
      
      target_character_ids.append(target_character_id)

    return target_character_ids
