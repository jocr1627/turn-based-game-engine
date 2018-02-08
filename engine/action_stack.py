class ActionStack:
  def __init__(self, stack=[]):
    self.ids_to_keys = {}
    self.keys_to_ids = {}
    self.stack = []

    for action in stack:
      self.push(action)

  def __contains__(self, action):
    return action in self.stack
  
  def __getitem__(self, key):
    return self.stack[key]
  
  def __len__(self):
    return len(self.stack)
  
  def get_key(self, action):
    name = action.get_name()
    parent_id = action.parent and action.parent.id

    return (name, parent_id)
  
  def is_cycle(self, action):
    return self.get_key(action) in self.keys_to_ids

  def pop(self):
    action = self.stack.pop()
    key = self.ids_to_keys[action.id]

    self.keys_to_ids[key].remove(action.id)

    if len(self.keys_to_ids[key]) == 0:
      del self.keys_to_ids[key]
    
    del self.ids_to_keys[action.id]

    return action

  def push(self, action):
    key = self.get_key(action)

    if key not in self.keys_to_ids:
      self.keys_to_ids[key] = set()
    
    self.keys_to_ids[key].add(action.id)
    self.ids_to_keys[action.id] = key
    self.stack.append(action)
