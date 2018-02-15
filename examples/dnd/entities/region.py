from examples.dnd.entities.location import Location

class Region(Location):
  def __init__(self, name, locations=[], neighbors=[]):
    super().__init__(name, children=locations, neighbors=neighbors)
