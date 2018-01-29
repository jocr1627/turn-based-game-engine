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
