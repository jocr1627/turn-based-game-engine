from examples.dnd.entities.character import Character

def get_characters_in_range(reference_location, max_range):
  region = reference_location.parent
  stack = [(reference_location, 0)]
  valid_locations = set()

  while len(stack) > 0:
    location,distance = stack.pop()
    valid_locations.add(location)
    
    if max_range < 0 or distance < max_range:
      for neighbor in location.hydrate('neighbor_ids'):
        if neighbor.parent is not region and neighbor.parent.id not in region.get('neighbor_ids'):
          continue

        if neighbor not in valid_locations:
          stack.append((neighbor, distance + 1))

  valid_character_ids = []

  for location in valid_locations:
    valid_character_ids += [
      entity.id for entity in location.children.values()
      if isinstance(entity, Character) and entity is not character
    ]

  return valid_character_ids
