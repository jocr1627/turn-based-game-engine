from engine.deep_merge import deep_merge
from engine.diff import Diff
from engine.state import State

class Entity:
  next_entity_id = 0

  def __init__(self, children=[], entity_classes={}, parent=None, state={}):
    self.descendants = {}
    self.diffs = []
    self.entity_classes = entity_classes
    self.listeners = {}
    self.parent = None
    self.root = self

    self.id = Entity.next_entity_id
    Entity.next_entity_id += 1
    
    if parent is not None:
      parent.add_child(self)
    
    self.children = {}
    children_list = self.get_default_children() + children

    for child in children_list:
      self.add_child(child)

    raw_state = deep_merge(self.get_default_state(), state)
    self.state = State(raw_state)
  
  def __hydrate__(self, value):
    if type(value) is list or type(value) is set:
      hydrated_values = []

      for entity_id in value:
        entity = None

        if entity_id in self.root.descendants:
          entity = self.root.descendants[entity_id]
        
        hydrated_values.append(entity)
      
      return hydrated_values
    elif value in self.root.descendants:
      return self.root.descendants[value]

  def add_child(self, child, diff=Diff()):
    if child.id not in self.children:
      if child.parent is not None:
        child.parent.remove_child(child)

      self.children[child.id] = child
      child.parent = self
      child.root = self.root
      self.root.descendants[child.id] = child

      if hasattr(child, 'get_should_react'):
        self.root.listeners[child.id] = child

      for descendant_id in child.descendants:
        descendant = child.descendants[descendant_id]
        self.root.descendants[descendant_id] = descendant
        descendant.root = self.root

      for listener_id in child.listeners:
        self.root.listeners[listener_id] = child.listeners[listener_id]

      child.descendants = {}
      child.listeners = {}

      if len(self.root.diffs) > 0:
        diff.setIn(['children', self.id, child.id], (None, child))
  
  def end_diff(self):
    return self.diffs.pop()
  
  def get(self, key):
    return self.state.get(key)
  
  def getIn(self, keys):
    return self.state.getIn(keys)

  def get_default_children(self):
    return []

  def get_default_state(self):
    return {}

  def get_descendants(self, descendants={}):
    for child in self.children.values():
      descendants[child.id] = child
      descendants = child.get_descendants(descendants)
    
    return descendants

  @classmethod
  def get_name(clazz):
    return clazz.__name__

  def has(self, key):
    return self.state.has(key)
  
  def hasIn(self, keys):
    return self.state.hasIn(keys)
  
  def hydrate(self, key):
    return self.__hydrate__(self.get(key))
  
  def hydrateIn(self, keys):
    return self.__hydrate__(self.getIn(keys))

  def inspect(self, key, getter):
    return self.state.inspect(key, getter)
  
  def inspectIn(self, keys, getter):
    return self.state.inspectIn(keys, getter)

  def mutate(self, key, mutation):
    original_value = self.state.get(key)
    self.state.mutate(key, mutation)
    value = self.state.__get__(key)
    
    if len(self.root.diffs) > 0:
      diff = self.root.diffs[-1]
      diff.setIn(['state', self.id, key], (original_value, value))
  
  def mutateIn(self, keys, mutation):
    original_value = self.state.getIn(keys)
    self.state.mutateIn(keys, mutation)
    value = self.state.__getIn__(keys)
    
    if len(self.root.diffs) > 0:
      diff = self.root.diffs[-1]
      diff.setIn(['state', self.id, *keys], (original_value, value))

  def remove_child(self, child, diff=Diff()):
    if child.id in self.children:
      child.parent = None
      del self.children[child.id]
      del self.root.descendants[child.id]
      child.root = child
      child.descendants = child.get_descendants()
      child.listeners = {}

      if child.id in self.root.listeners:
        del self.root.listeners[child.id]

      for descendant_id in child.descendants:
        del self.root.descendants[descendant_id]
        descendant = child.descendants[descendant_id]
        descendant.root = child

        if hasattr(descendant, 'get_should_react'):
          child.listeners[descendant.id] = descendant

      if len(self.root.diffs) > 0:
        diff.setIn(['children', self.id, child.id], (child, None))
  
  def set(self, key, value):
    original_value = self.state.get(key)
    self.state.set(key, value)
    
    if len(self.root.diffs) > 0:
      diff = self.root.diffs[-1]
      diff.setIn(['state', self.id, key], (original_value, value))
  
  def setIn(self, keys, value):
    original_value = self.state.getIn(keys)
    self.state.setIn(keys, value)
    
    if len(self.root.diffs) > 0:
      diff = self.root.diffs[-1]
      diff.setIn(['state', self.id, *keys], (original_value, value))
  
  def start_diff(self):
    diff = Diff()
    self.diffs.append(diff)

    return diff

  def update(self, key, updater):
    original_value = self.state.get(key)
    self.state.update(key, updater)
    value = self.state.__get__(key)
    
    if len(self.root.diffs) > 0:
      diff = self.root.diffs[-1]
      diff.setIn(['state', self.id, key], (original_value, value))
  
  def updateIn(self, keys, updater):
    original_value = self.state.getIn(keys)
    self.state.updateIn(keys, updater)
    value = self.state.__getIn__(keys)
    
    if len(self.root.diffs) > 0:
      diff = self.root.diffs[-1]
      diff.setIn(['state', self.id, *keys], (original_value, value))
