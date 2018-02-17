import re
from examples.dnd.entities.character import Character

class Player(Character):
  def get_ability_id(self, args):
    abilities = self.hydrate('abilities')
    name = self.get('name')
    ability_id = None

    while ability_id is None:
      action_name = input(f'Enter an action for player {name}: ').lower()
      is_match_found = False

      for ability in abilities.values():
        if re.match(ability.matcher, action_name):
          is_match_found = True

          if ability.get_is_possible():
            ability_id = ability.id
          else:
            print(f'{name} is not able to perform {action_name} at this time.')

          break
      
      if not is_match_found:
        print(f'{action_name} does match any known abilities. Options include: {list(abilities.keys())} Try again.')
    
    return ability_id

  def get_roll(self, args):
    action_id = args['action_id']
    roll_type = args['roll_type']
    action = self.hydrate_by_id(action_id)
    action_name = action.get_name()
    name = self.get('name')
    roll = None

    while roll is None:
      raw_roll = input(f'Enter {name}\'s total {roll_type} roll for {action_name}: ')

      try:
        roll = int(raw_roll)
      except ValueError:
        print(f'{raw_roll} is not a valid roll.')

    return (roll, roll)

  def get_target_character_ids(self, args):
    return self.get_target_ids('character', args)
  
  def get_target_ids(self, target_type, args):
    action_id = args['action_id']
    action = self.hydrate_by_id(action_id)
    action_name = action.get_name()
    num_targets = args['num_targets']
    valid_ids = args['valid_ids']
    valid_targets = [self.hydrate_by_id(target_id) for target_id in valid_ids]
    valid_target_ids_by_name = { target.get('name').lower(): target.id for target in valid_targets }
    name = self.get('name')
    target_ids = []

    for i in range(num_targets):
      target_id = None

      while target_id is None:
        target_name = input(f'Enter a target {target_type} for {name}\'s {action_name}: ').lower()

        if target_name in valid_target_ids_by_name:
          target_id = valid_target_ids_by_name[target_name]
        else:
          print(f'{target_name} is not a valid target {target_type}. Options include: {list(valid_target_ids_by_name.keys())} Try again.')
      
      target_ids.append(target_id)

    return target_ids

  def get_target_location_ids(self, args):
    return self.get_target_ids('location', args)
