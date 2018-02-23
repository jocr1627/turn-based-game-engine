def get_location_distance(location1, location2):
  searched = set()
  search_stack = [(location1, 0)]
  distance = None

  while distance is None and len(search_stack) > 0:
    location,current_distance = search_stack.pop()
    searched.add(location.id)

    if location is location2:
      distance = current_distance
    else:
      neighbors = location.get_neighbors()
      search_stack += [(neighbor, current_distance + 1) for neighbor in neighbors if neighbor.id not in searched]

  return distance
