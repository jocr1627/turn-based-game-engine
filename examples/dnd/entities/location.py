from engine.entity import Entity

class Location(Entity):
  def __init__(self, name, neighbors=[]):
    super().__init__(state={ 'name': name })

    for neighbor in neighbors:
      self.add_edge(neighbor)

  def add_edge(self, neighbor):
    self.mutate('neighbor_ids', lambda neighbor_ids: neighbor_ids.add(neighbor.id))
    neighbor.mutate('neighbor_ids', lambda neighbor_ids: neighbor_ids.add(self.id))

  def get_default_state(self):
    return { 'neighbor_ids': set() }

  def remove_edge(self, neighbor):
    self.mutate('neighbor_ids', lambda neighbor_ids: neighbor_ids.remove(neighbor.id))
    neighbor.mutate('neighbor_ids', lambda neighbor_ids: neighbor_ids.remove(self.id))
