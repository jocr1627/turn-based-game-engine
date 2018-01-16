class Entity:
  next_entity_id = 0

  def __init__(self, game, children=None, reactions=None, state=None):
    self.children = {}
    self.does_exist = True
    self.id = Entity.next_entity_id
    self.game = game
    self.parent = None
    self.reactions = reactions if reactions is not None else self.get_default_reactions(game)
    self.state = state if state is not None else self.get_default_state(game)

    children = children if children is not None else self.get_default_children(game)
    
    for child in children:
      self.add_child(child)
    
    Entity.next_entity_id += 1

  def add_child(self, child):
    self.children[child.id] = child
    child.parent = self

  def get_default_children(self, game):
    return []

  def get_default_reactions(self, game):
    return []

  def get_default_state(self, game):
    return {}

  def get_descendants(self):
    descendants = []

    for child in self.children.values():
      descendants.append(child)
      descendants += child.get_descendants()
    
    return descendants
  
  def remove_child(self, child):
    child.does_exist = False
    child.parent = None
    del self.children[child.id]

  def update(self, diffs):
    return
