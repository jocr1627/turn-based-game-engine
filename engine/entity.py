from copy import deepcopy

class State:
  def __init__(self, entity_id, raw_state={}):
    self.entity_id = entity_id
    self.raw_state = raw_state
  
  def __contains__(self, key):
    return key in self.raw_state

  def get(self, key):
    return deepcopy(self.raw_state[key]) if key in self.raw_state else None
  
  def set(self, key, value, diffs={}):
    new_diffs = deepcopy(diffs)
 
    if issubclass(value.__class__, Entity):
      print('Warning: You attempted to set state: {key} {value} Do not set entities to state. Defaulting to id.')
      value = value.id
    
    original_value = self.get(key)
    self.raw_state[key] = value

    if self.entity_id not in new_diffs:
      new_diffs[self.entity_id] = {}
    
    new_diffs[self.entity_id][key] = (original_value, value)

    return new_diffs

class Entity:
  next_entity_id = 0

  def __init__(self, game, children=None, reactions=None, state=None):
    self.children = {}
    self.does_exist = True
    self.id = Entity.next_entity_id
    self.game = game
    self.parent = None
    self.reactions = reactions if reactions is not None else self.get_default_reactions(game)
    
    raw_state = state if state is not None else self.get_default_state(game)
    self.state = State(self.id, raw_state)

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
