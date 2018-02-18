from engine.deep_merge import deep_merge
from engine.entity import Entity

class Region(Entity):
  def __init__(self, name, locations=[], neighbors=[]):
    super().__init__(children=locations, state={ 'name': name })

    for neighbor in neighbors:
      self.add_edge(neighbor)

  def add_edge(self, neighbor):
    self.mutate('neighbor_ids', lambda neighbor_ids: neighbor_ids.add(neighbor.id))
    neighbor.mutate('neighbor_ids', lambda neighbor_ids: neighbor_ids.add(self.id))

  def get_default_state(self):
    return deep_merge(
      super().get_default_state(),
      { 'neighbor_ids': set() }
    )

  def remove_edge(self, neighbor):
    self.mutate('neighbor_ids', lambda neighbor_ids: neighbor_ids.remove(neighbor.id))
    neighbor.mutate('neighbor_ids', lambda neighbor_ids: neighbor_ids.remove(self.id))
