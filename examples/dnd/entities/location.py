from engine.deep_merge import deep_merge
from engine.entity import Entity

class Location(Entity):
  parent_alias = 'region'

  def __init__(self, name, neighbors=[]):
    super().__init__(state={ 'name': name })

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

  def get_neighbors(self):
    return self.hydrate('neighbor_ids')

  def remove_edge(self, neighbor):
    self.mutate('neighbor_ids', lambda neighbor_ids: neighbor_ids.remove(neighbor.id))
    neighbor.mutate('neighbor_ids', lambda neighbor_ids: neighbor_ids.remove(self.id))

  def validate_parent(self, parent):
    if not parent.is_type('Region'):
      raise ValueError(f'Invalid parent for {self.__class__.__name__}. Expected Region but got {parent.__class__.__name__}.')
