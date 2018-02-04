class ActionStack:
  def __init__(self):
    self.map = {}
    self.stack = []

  def __contains__(self, action):
    key = self.get_key(action)

    return key in self.map and action.id in self.map[key]
  
  def __getitem__(self, key):
    return self.stack[key]
  
  def __len__(self):
    return len(self.stack)
  
  def get_key(self, action):
    name = action.get_name()
    parent_id = action.parent and action.parent.id

    return (name, parent_id)
  
  def is_cycle(self, action):
    return self.get_key(action) in self.map

  def pop(self):
    action = self.stack.pop()
    key = self.get_key(action)

    self.map[key].remove(action.id)

    if len(self.map[key]) == 0:
      del self.map[key]

    return action

  def push(self, action):
    key = self.get_key(action)

    if key not in self.map:
      self.map[key] = set()
    
    self.map[key].add(action.id)
    self.stack.append(action)
