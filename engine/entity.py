from engine.base_listener import BaseListener
from engine.deep_merge import deep_merge
from engine.diff import Diff
from engine.state import State

class Entity:
  next_entity_id = 0

  def __init__(self, children=[], game=None, getters={}, parent=None, state={}):
    self.game = game
    self.getters = deep_merge(self.get_default_getters(), getters)
    self.parent = None

    self.id = Entity.next_entity_id
    Entity.next_entity_id += 1
    
    inheritor_stack = [self]
    raw_state = state

    while len(inheritor_stack) > 0:
      inheritor = inheritor_stack.pop()
      raw_state = deep_merge(inheritor.get_default_state(), raw_state)
      clazz = inheritor.__thisclass__ if isinstance(inheritor, super) else inheritor.__class__
      supers = [super(base, self) for base in clazz.__bases__]
      inheritor_stack += [zuper for zuper in supers if hasattr(zuper, 'get_default_state')]

    self.state = State(raw_state)
        
    self.children = {}
    children_list = self.get_default_children() + children

    for child in children_list:
      self.add_child(child)
    
    if parent is not None:
      parent.add_child(self)
  
  def add_child(self, child):
    if child.id not in self.children:
      if child.parent is not None:
        child.parent.remove_child(child)

      self.children[child.id] = child
      child.game = self.game
      child.parent = self
      self.register_descendant(child)
      
      for descendant in child.get_descendants([]):
        self.register_descendant(descendant)

      self.update_diff(['children', self.id, child.id], False, True)

  def end_diff(self):
    return self.diffs.pop()
  
  def get(self, key):
    return self.state.get(key)
  
  def get_in(self, keys):
    return self.state.get_in(keys)

  def get_default_children(self):
    return []
  
  def get_default_getters(self):
    return {}

  def get_default_state(self):
    return {}

  def get_descendants(self, descendants):
    for child in self.children.values():
      descendants.append(child)
      descendants = child.get_descendants(descendants)
    
    return descendants

  @classmethod
  def get_name(clazz):
    return clazz.__name__

  def has(self, key):
    return self.state.has(key)
  
  def has_in(self, keys):
    return self.state.has_in(keys)
  
  def hydrate(self, key):
    return self.hydrate_by_id(self.get(key))

  def hydrate_by_id(self, id_or_ids):
    if self.game is None:
      raise Exception(f'Cannot hydrate values when game is unassigned: {self.get_name()} {self.id}')

    if type(id_or_ids) is list or type(id_or_ids) is set:
      hydrated_values = []

      for entity_id in id_or_ids:
        entity = None

        if entity_id in self.game.descendants:
          entity = self.game.descendants[entity_id]
        
        hydrated_values.append(entity)
      
      return hydrated_values
    elif id_or_ids in self.game.descendants:
      return self.game.descendants[id_or_ids]

  def hydrate_in(self, keys):
    return self.hydrate_by_id(self.get_in(keys))

  def inspect(self, key, getter):
    return self.state.inspect(key, getter)
  
  def inspect_in(self, keys, getter):
    return self.state.inspect_in(keys, getter)

  def mutate(self, key, mutater):
    original_value = self.state.get(key)
    self.state.mutate(key, mutater)
    value = self.state.__get__(key)
    self.update_diff(['state', self.id, key], original_value, value)

  def mutate_in(self, keys, mutater):
    original_value = self.state.get_in(keys)
    self.state.mutate_in(keys, mutater)
    value = self.state.__get_in__(keys)
    self.update_diff(['state', self.id, *keys], original_value, value)

  def register_descendant(self, descendant):
    descendant.game = self.game

    if self.game is not None:
      self.game.descendants[descendant.id] = descendant

      if isinstance(descendant, BaseListener):
        self.game.listeners[descendant.id] = descendant

  def remove_child(self, child):
    if child.id in self.children:
      child.parent = None
      del self.children[child.id]
      self.unregister_descendant(child)

      for descendant in child.get_descendants([]):
        self.unregister_descendant(descendant)

      self.update_diff(['children', self.id, child.id], True, False)

  def set(self, key, value):
    original_value = self.state.get(key)
    self.state.set(key, value)
    self.update_diff(['state', self.id, key], original_value, value)
  
  def set_in(self, keys, value):
    original_value = self.state.get_in(keys)
    self.state.set_in(keys, value)
    self.update_diff(['state', self.id, *keys], original_value, value)
  
  def start_diff(self):
    diff = Diff()
    self.diffs.append(diff)

    return diff
  
  def update_diff(self, keys, original_value, value):
    if self.game is not None and len(self.game.diffs) > 0:
      diff = self.game.diffs[-1]
      diff.set_in(keys, (original_value, value))

  def update(self, key, updater):
    original_value = self.state.get(key)
    self.state.update(key, updater)
    value = self.state.__get__(key)
    self.update_diff(['state', self.id, key], original_value, value)

  def update_in(self, keys, updater):
    original_value = self.state.get_in(keys)
    self.state.update_in(keys, updater)
    value = self.state.__get_in__(keys)
    self.update_diff(['state', self.id, *keys], original_value, value)

  def unregister_descendant(self, descendant):
    descendant.game = None

    if self.game is not None:
      del self.game.descendants[descendant.id]

      if descendant.id in self.game.listeners:
        del self.game.listeners[descendant.id]
