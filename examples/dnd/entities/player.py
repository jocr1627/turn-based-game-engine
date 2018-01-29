class Player(Character):
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
