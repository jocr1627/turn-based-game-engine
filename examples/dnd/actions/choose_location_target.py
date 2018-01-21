from engine.action import Action

class ChooseLocationTarget(Action):
  def execute(self, diff):
    name = self.parent.parent.get('name')
    current_location = self.parent.parent.parent
    neighbors = current_location.hydrate('neighbor_ids')
    neighbors_by_name = { neighbor.get('name').lower(): neighbor.id for neighbor in neighbors }
    target_location_id = None

    while target_location_id is None:
      target_location_name = input(f'Enter {name}\'s target location: ').lower()

      if target_location_name in neighbors_by_name:
        target_location_id = neighbors_by_name[target_location_name]
      else:
        print(f'{target_location_name} is not a valid location. Options include: {list(neighbors_by_name.keys())} Try again.')
    
    action = self.hydrate('action_id')
    action.set('target_location_id', target_location_id)
